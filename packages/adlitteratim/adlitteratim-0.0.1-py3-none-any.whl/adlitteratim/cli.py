import os
import click
from ruamel.yaml import YAML

# Config directories
CONFIG_DIR = os.path.expanduser("~/.adlitteratim")
PROMPTS_DIR = os.path.join(CONFIG_DIR, "prompts")
TESTS_DIR = os.path.join(CONFIG_DIR, "tests")

@click.group()
def main():
    """adlitteratim: CLI to manage LLM prompts ad litteratim (letter‑by‑letter)."""
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)

@main.command()
@click.argument("name")
def new(name):
    """Create a new prompt scaffold: adlitteratim new <name>"""
    yaml = YAML()
    prompt_path = os.path.join(PROMPTS_DIR, f"{name}.yml")
    skeleton = {
        "description": "<Describe intent here>",
        "template": "|-\n  <Your prompt with {{ placeholders }}>"
    }
    with open(prompt_path, "w") as f:
        yaml.dump(skeleton, f)
    click.echo(f"Created prompt scaffold: {prompt_path}")

@main.command()
def lint():
    """Lint all prompts against token budget & placeholder syntax."""
    click.echo("Linting prompts... (not yet implemented)")

@main.command()
@click.argument("name", required=False)
def test(name):
    """Run prompt tests (all or for a specific NAME)."""
    click.echo(f"Running tests for '{name or 'all prompts'}'... (not yet implemented)")

@main.command()
@click.argument("name")
@click.option("--ref", default="main", help="Git ref to diff against")
def diff(name, ref):
    """Show diff for a prompt versus REF."""
    click.echo(f"Diffing '{name}' against '{ref}'... (not yet implemented)")

@main.command()
def package():
    """Bundle prompts/tests for sharing."""
    click.echo("Packaging artifact... (not yet implemented)")

@main.command("ci-setup")
def ci_setup():
    """Emit GitHub Actions snippet for CI integration."""
    click.echo("Generating CI template... (not yet implemented)")

if __name__ == "__main__":
    main()
