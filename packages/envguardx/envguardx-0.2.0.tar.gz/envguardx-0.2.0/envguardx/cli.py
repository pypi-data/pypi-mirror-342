from typing import Optional
import click
from .checker import check_env_file, generate_env_example


@click.group()
def main() -> None:
    """envguard - validate and manage .env files"""
    pass


@main.command()
@click.argument("env_path", type=click.Path(exists=True))
@click.option("--schema", "-s", "schema_path", type=click.Path(exists=True), help="Path to .env schema JSON file")
def check(env_path: str, schema_path: Optional[str]) -> None:
    """Check .env file for completeness and unsafe values."""
    issues = check_env_file(env_path, schema_path)
    if issues:
        click.secho("Issues found:", fg="red", bold=True)
        for issue in issues:
            click.echo(f"- {issue}")
    else:
        click.secho("No issues found. ✅", fg="green", bold=True)



@main.command()
@click.argument("env_path", type=click.Path(exists=True))
@click.option("--output", "-o", default=".env.example", help="Output file name")
def generate(env_path: str, output: str) -> None:
    """Generate .env.example from a .env file."""
    generate_env_example(env_path, output)
    click.secho(f"Generated example file: {output}", fg="green")
