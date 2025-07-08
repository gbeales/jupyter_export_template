"""Command-line interface for jupyter-export-template."""

import click
from pathlib import Path
from typing import Optional

from .exporter import NotebookExporter


@click.command()
@click.argument('input_notebook', type=click.Path(exists=True, path_type=Path), required=False)
@click.argument('output_file', type=click.Path(path_type=Path), required=False)
@click.option(
    '--template', '-t',
    default='default.j2',
    help='Template file to use for export (default: default.j2)'
)
@click.option(
    '--template-dir',
    type=click.Path(exists=True, path_type=Path),
    help='Directory containing custom templates'
)
@click.option(
    '--config', '-c',
    type=click.Path(exists=True, path_type=Path),
    help='YAML configuration file for batch export'
)
@click.option(
    '--list-templates',
    is_flag=True,
    help='List available templates and exit'
)
@click.version_option(version='0.1.0')
def main(
    input_notebook: Optional[Path],
    output_file: Optional[Path],
    template: str,
    template_dir: Optional[Path],
    config: Optional[Path],
    list_templates: bool
):
    """Export Jupyter notebooks using Jinja2 templates.

    INPUT_NOTEBOOK: Path to the input .ipynb file
    OUTPUT_FILE: Path where the exported file will be saved
    """
    # Initialize exporter
    exporter = NotebookExporter(template_dir=template_dir)

    # List templates if requested
    if list_templates:
        available_templates = exporter.get_available_templates()
        if available_templates:
            click.echo("Available templates:")
            for tmpl in available_templates:
                click.echo(f"  - {tmpl}")
        else:
            click.echo("No templates found.")
        return

    # Export using config file
    if config:
        try:
            exporter.export_with_config(config)
            click.echo(f"Exported notebooks using config: {config}")
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise click.Abort()
        return

    # Check if required arguments are provided for single notebook export
    if not input_notebook or not output_file:
        click.echo("Error: INPUT_NOTEBOOK and OUTPUT_FILE are required unless using --list-templates or --config")
        raise click.Abort()

    # Single notebook export
    try:
        exporter.export_notebook(
            notebook_path=input_notebook,
            output_path=output_file,
            template=template
        )
        click.echo(f"Exported {input_notebook} to {output_file}")
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    main()
