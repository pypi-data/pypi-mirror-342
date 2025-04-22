"""
Command-line interface for PyHTKLib.
"""

import click
from .osciloskop.jobs import measurement_job, parse_configurations
from .osciloskop.core import Oscilloscope
from . import __version__

@click.group()
@click.version_option(version=__version__)
def cli():
    """PyHTKLib - Hantek Oscilloscope Control Library"""
    pass

@cli.command()
def test():
    """Test the PyHTKLib components"""
    print("Testing PyHTKLib components:")
    # Add test implementation here

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
def measure(config_file):
    """Run measurements using the specified configuration file"""
    configurations = parse_configurations(config_file)
    measurement_job(configurations)

if __name__ == '__main__':
    cli() 