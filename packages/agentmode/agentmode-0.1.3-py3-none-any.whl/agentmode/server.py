import click
import httpx

@click.command()
def cli():
    """Prints a greeting."""
    click.echo("Hello, World!")