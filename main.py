import click
import yaml
from watcher import start_watching

@click.group()
def cli():
    """A tool to automatically sort files from a staging area."""
    pass

@cli.command()
@click.option('--config', default='config.yaml', help='Path to the configuration file.')
def start(config):
    
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
        
        start_watching(config_data)
    except FileNotFoundError:
        click.echo(f"Error: Configuration file not found at '{config}'")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

if __name__ == '__main__':
    cli()