from dataclasses import dataclass
from functools import partial
from toolz import mapcat
from copy import deepcopy
from pathlib import Path
import ujson as json
from hypothesis import example, given, strategies as st
from hypothesis_jsonschema import from_schema
from .utils import offset_date

@dataclass(frozen=True)
class ClaimScenario:
    base_profile: dict
    claim_type: str
    scenario: dict # the scenario for the claim type
    
@dataclass(frozen=True)
class SchemasByClaimType:
    ac: dict
    il: dict


# ---------- Utils -----------------------------------------------------------------
def get_all_date_kvpairs(json: dict):
    """
    Extracts a set of (key, value) pairs, where the value is a date string,
    from a json dict
    
    EG: 
    >>> get_all_date_kvpairs(base_profile)
    {('blah_date', '2001-11-10'), ('blah2_date', '2000-06-15')}
    """
    pairs = set()
     
    for key, value in json.items():
        if isinstance(value, str) and (key.endswith("_date") or key.endswith("_dt")):
            pairs.add((key, value))
        if isinstance(value, dict):
            pairs.update(get_all_date_kvpairs(json[key]))
        if isinstance(value, list):
            for elt in value:
                if isinstance(elt, dict): 
                    pairs.update(get_all_date_kvpairs(elt))
    return pairs

def dates_from_base_profile(bp: dict) -> set:
    return {date for _, date in get_all_date_kvpairs(bp)}

def prohibit_additional_properties(schema: dict):
    """
    Recursively adds "additionalProperties": false to every object in the JSON schema,
    so that won't get additional props in generated data
    """
    if isinstance(schema, dict):
        new_schema = {
            key: prohibit_additional_properties(value) for key, value in schema.items()
        }
        # want to recursively do this for every dict, even if dict is not obj
        if schema.get('type') == 'object':
            new_schema['additionalProperties'] = False
        return new_schema
    elif isinstance(schema, list):
        return [prohibit_additional_properties(item) for item in schema]
    else:
        # Return the item as is if it's neither a dictionary nor a list
        return schema

# ---------------------------------------------------------------------------------------

# ---------- Base profiles ---------------------------------------------------------
def init_base_profiles_st(base_profiles: list[dict]) -> st.SearchStrategy:
    base_profiles = [(idx, profile) for idx, profile in enumerate(base_profiles)]
    return st.sampled_from(base_profiles)

# ---------------------------------------------------------------------------------------

# ---------- Getting the right schema for the claim type -----------------------------
def get_schemas_for_claim_types(form_schema: dict) -> dict:
    schema_ac = get_schema_for_claim_type(form_schema, "Ac")
    schema_il = get_schema_for_claim_type(form_schema, "Il")
    return SchemasByClaimType(ac=schema_ac, il=schema_il)


def remove_other_claim_subschemas(schema: dict, claim_type: str):
    """ 
    Returns a schema that doesn't have the stuff for the other claim path in the Web_Form 
    (which should be enough for hypothesis_jsonschema to not generate data for that path)
    Annoying opportunities for edge cases regarding mutation and python's treatment of `filter` to rear their head here 
    """
    def get_the_other_claim_type(claim_type: str):
        if claim_type.startswith("Ac"): return "il"
        elif claim_type.startswith("Il"): return "ac"
        else: raise Exception(f"Unknown claim type {claim_type}")

    schema = deepcopy(schema)
    to_remove = list(filter(lambda k: 
                                     k.startswith(get_the_other_claim_type(claim_type)), 
                           schema["$defs"]["Web_Form"]["properties"].keys()))
    schema["$defs"]["Web_Form"]["properties"] = {k: v for k, v in schema["$defs"]["Web_Form"]["properties"].items() if k not in to_remove}
    return schema

def get_schema_for_claim_type(orig_schema: dict, claim_type: str) -> dict:
    """
    where `claim_type` is one of the values of the `Claim` enum in the schema
    """
    schema = deepcopy(orig_schema)
    del schema["$defs"]["Web_Form"]["properties"]["claim_type"]
    del schema["$defs"]["Claim"]

    # this is implemented in a somewhat roundabout way to avoid revealing the exact claim type strings
    if claim_type.startswith("Ac") or claim_type.startswith("Il"):
        schema = remove_other_claim_subschemas(schema, claim_type)
    else:
        raise Exception(f"Unknown claim type {claim_type}")
    
    return schema

@st.composite
def claim_scenario_st(draw, orig_schema: dict, base_profiles: list[dict]):
    """
    Given the original schema dict and base profiles, returns a strategy for ClaimScenarios

    We need to first draw from the type of claim, 
    then massage the original schema into the right form for the claim type
    """
    # Set up schemas and base profiles and related strats
    orig_schema = prohibit_additional_properties(orig_schema)
    schs_by_claim_type = get_schemas_for_claim_types(orig_schema)

    dates_per_bp = [dates_from_base_profile(bp) for bp in base_profiles]
    base_profiles_st = init_base_profiles_st(base_profiles)

    # 1. first draw from (i) base profiles and (ii) the type of claim
    base_profile_idx_pair = draw(base_profiles_st)
    bp_dates = list(dates_per_bp[base_profile_idx_pair[0]])

    claim_type_enum_sch = orig_schema["$defs"]["Claim"]
    claim_type = draw(from_schema(claim_type_enum_sch)).lower()
    
    # 2. sample data from the schema for that claim type,
    #    and given the dates in the base profile
    date_st_for_bp = st.sampled_from(bp_dates) | st.dates().map(str)

    if claim_type.startswith("ac"): 
        claim_schema = schs_by_claim_type.ac
    elif claim_type.startswith("il"):
        claim_schema = schs_by_claim_type.il
    else:
        raise Exception(f"Unknown claim type {claim_type}")

    scenario = draw(from_schema(claim_schema,
                                custom_formats={"date": date_st_for_bp}))

    return ClaimScenario(base_profile = base_profile_idx_pair,
                        claim_type=claim_type, 
                        scenario=scenario)
