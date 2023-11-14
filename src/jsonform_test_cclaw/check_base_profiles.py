from toolz import compose, curry
from toolz.functoolz import pipe
from functools import partial

import typer
from pathlib import Path
import ujson as json

# Keep name to make logs more comprehensible
UI_ONLY_FIELDS = ["add_ons", 
                  "address",
                  "contract_currency",
                  "contract_type",
                  "ic_number",
                  "occupation",
                  "policy_number",
                  "sex"]
def remove_ui_fields(profile: dict) -> dict:
    """
    Remove fields that are only used for the UI
    """
    return {k: v for k, v in profile.items() if k not in UI_ONLY_FIELDS}

def get_profile_array(orig_base_profiles: dict) -> list:
    """
    Base profiles json -> cleaner array of profiles, 
    where the 0th entry is the 0th user and so forth
    """
    userkeys = [str(i) for i in range(len(orig_base_profiles["user"]))]
    profile_array = [orig_base_profiles["user"][user] for user in userkeys]
    return profile_array

def check_base_profiles_internal_consistent(profiles: list[dict]):
    """
    [NOT YET IMPLEMENTED] Check base user profiles json for internal inconsistencies.
    """    
    pass

def is_risk_commencement_date_after_dob(profile: dict) -> bool:
    pass

def is_num_stepups_valid(profile: dict) -> bool:
    pass

def is_past_claims_valid(profile: dict) -> bool:
    pass


def extract_profiles_from_path(base_profiles_path: Path):
    with open(base_profiles_path, "r") as base_profiles_file: 
        base_profiles = pipe(base_profiles_file, 
                                json.load,
                                get_profile_array,
                                partial(map, remove_ui_fields),
                                list)
    return base_profiles
