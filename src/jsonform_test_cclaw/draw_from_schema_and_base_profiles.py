from functools import partial
from copy import deepcopy
from pathlib import Path
import ujson as json
from dataclasses import dataclass

from hypothesis import example, given, strategies as st
from hypothesis_jsonschema import from_schema

@dataclass
class ClaimScenario:
    claim_type: str
    scenario: dict # the scenario for the claim type

@st.composite
def claim_scenario_st(draw, orig_schema: dict):
    """
    We need to first draw from the type of claim, 
    then massage the original schema into the right form for the claim type
    """
    subschema_for_claim_type = partial(get_schema_for_claim_type, orig_schema)

    # 1. first draw from the type of claim
    claim_type_enum_sch = orig_schema["$defs"]["Claim"]
    claim_type = draw(from_schema(claim_type_enum_sch))


    # TODO: OK I think I need to traverse the schema more manually 
    # Also check how to pass options, e.g. for dates
    # Might want to sample from Meng's jsonranges --- look into that

    # 2. massage the original schema into the right form for the claim type, and then sample data from it
    raise Exception("NOT YET IMPLEMENTED")

    # schema_for_claim_type = subschema_for_claim_type(claim_type)
    # scenario = draw(from_schema(schema_for_claim_type))

    return ClaimScenario(claim_type=claim_type, scenario=scenario)

def get_the_other_claim_type(claim_type: str):
    if claim_type.startswith("A"): return "I"
    elif claim_type.startswith("I"): return "A"
    else: raise Exception(f"Unknown claim type {claim_type}")

def get_schema_for_claim_type(orig_schema: dict, claim_type: str) -> dict:
    """
    where `claim_type` is one of the values of the `Claim` enum in the schema
    """
    schema = deepcopy(orig_schema["$defs"])
    del schema["Web_Form"] 
    del schema["Claim"]

    # this is implemented in a somewhat roundabout way to avoid revealing the exact claim type strings
    if claim_type.startswith("A"): 
        to_remove = filter(lambda k: 
                            k.startswith(get_the_other_claim_type("A")), schema.keys())
        schema = {k: v for k, v in schema.items() if k not in to_remove}
    elif claim_type.startswith("Il"):
        to_remove = filter(lambda k: 
                            k.startswith(get_the_other_claim_type("Il")), schema.keys())
        schema = {k: v for k, v in schema.items() if k not in to_remove}
    else:
        raise Exception(f"Unknown claim type {claim_type}")

    # print(f"schema for claim type is {schema}\n")
    return schema


def sample_from_one_of_obj_props(obj: dict):
    pass



def init_base_profiles_st(base_profiles: list[dict]) -> st.SearchStrategy:
    base_profiles = [(idx, profile) for idx, profile in enumerate(base_profiles)]
    return st.sampled_from(base_profiles)


# form_schema_path = "../usecases/smu/public/json/preUser.json"
# claim_scenario_st(orig).example()

# test = from_schema({'type': 'string', 'format': 'date'})
# test.example()