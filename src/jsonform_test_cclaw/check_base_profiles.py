import typer
from pathlib import Path
import ujson as json

def check_base_profiles_internal_consistent(base_profiles_path: Path) -> bool:
    """
    [NOT YET IMPLEMENTED] Check base user profiles json for internal inconsistencies.
    """    
    with open(base_profiles_path, "r") as base_profiles_file: 
        profiles = json.load(base_profiles_file)

    # typer.echo(f"{profiles}")
    return True

def is_risk_commencement_date_after_dob(profile: dict) -> bool:
    pass

def is_num_stepups_valid(profile: dict) -> bool:
    pass

