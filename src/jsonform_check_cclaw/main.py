import typer
from typing import Optional
from pathlib import Path
from dataclasses import dataclass
from typing_extensions import Annotated
from typer_config.decorators import use_yaml_config  

app = typer.Typer()

@dataclass
class AppConfig:
    form_schema_path: Optional[Path] = None
    base_profiles_path: Optional[Path] = None
    form_app_path: Optional[Path] = None
    le_server_path: Optional[str] = None
    app_mode: str = "dev"



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


@app.command()
@use_yaml_config(default_value="../../config.yaml")
def main(
    form_schema: Annotated[Path, typer.Option()],
    base_user_profiles: Annotated[Path, typer.Option()],
    form_app: Annotated[Path, typer.Option()],
    le_server: Annotated[str, typer.Option()],
    mode: Annotated[str, typer.Option()]
):
    app_config = AppConfig(form_schema_path=form_schema,
                           base_profiles_path=base_user_profiles,
                           form_app_path=form_app,
                           le_server_path=le_server,
                           app_mode=mode)  
    typer.echo(f"{app_config}")

if __name__ == "__main__":
    app()
