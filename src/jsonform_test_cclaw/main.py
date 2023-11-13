import typer
from typing import Optional
from pathlib import Path
from dataclasses import dataclass
from typing_extensions import Annotated
from typer_config.decorators import use_yaml_config  

from .init_hyp import hyp_settings_load_profile
from .check_base_profiles import check_base_profiles_internal_consistent

app = typer.Typer()

# TODO: Think more about what should be optional -- not obvious that all of these are best modelled with Optional
@dataclass
class AppConfig:
    form_schema_path: Optional[Path] = None
    base_profiles_path: Optional[Path] = None
    form_app_path: Optional[Path] = None
    le_server_path: Optional[str] = None
    hypothesis_settings: Optional[str] = None

@app.command()
@use_yaml_config(default_value="./config.yaml")
def main(
    form_schema: Annotated[Path, typer.Option()],
    base_user_profiles: Annotated[Path, typer.Option()],
    form_app: Annotated[Path, typer.Option()],
    le_server: Annotated[str, typer.Option()],
    hypothesis_profile: Annotated[str, typer.Option()],
):
    hypothesis_settings = hyp_settings_load_profile(hypothesis_profile)  
    app_config = AppConfig(form_schema_path=form_schema,
                           base_profiles_path=base_user_profiles,
                           form_app_path=form_app,
                           le_server_path=le_server,
                           hypothesis_settings=hypothesis_settings)

    check_base_profiles_internal_consistent(app_config.base_profiles_path)
    
    typer.echo(f"{app_config}")

if __name__ == "__main__":
    app()


# @app.command("check-base-profiles")
# def check_base_profiles(
#     base_profiles_path: Path = typer.Argument(
#         "config.yaml", 
#         help="Path to the base user profiles json")
#     ):
#     """
#     [NOT YET IMPLEMENTED] Check base user profiles json for internal inconsistencies.
#     """    
#     typer.echo(f"{base_profiles_path}")
