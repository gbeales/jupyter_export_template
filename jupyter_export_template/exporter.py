"""Main exporter class for converting Jupyter notebooks using Jinja2 templates."""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union

import jinja2
import nbformat
import yaml

from .filters import setup_filters


class NotebookExporter:
    """Main class for exporting Jupyter notebooks using Jinja2 templates."""

    def __init__(self, template_dir: Optional[Union[str, Path]] = None):
        """Initialize the notebook exporter.

        Args:
            template_dir: Directory containing Jinja2 templates.
                         If None, uses built-in templates.
        """
        self.template_dir = self._get_template_dir(template_dir)
        self.env = self._setup_jinja_env()

    def _get_template_dir(self, template_dir: Optional[Union[str, Path]]) -> Path:
        """Get the template directory path."""
        if template_dir is None:
            # Use built-in templates
            package_dir = Path(__file__).parent
            return package_dir / "templates"
        return Path(template_dir)

    def _setup_jinja_env(self) -> jinja2.Environment:
        """Set up the Jinja2 environment with custom filters."""
        loader = jinja2.FileSystemLoader(str(self.template_dir))
        env = jinja2.Environment(
            loader=loader,
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Add custom filters
        setup_filters(env)

        return env

    def load_notebook(self, notebook_path: Union[str, Path]) -> nbformat.NotebookNode:
        """Load a Jupyter notebook from file.

        Args:
            notebook_path: Path to the notebook file.

        Returns:
            Loaded notebook object.
        """
        with open(notebook_path, 'r', encoding='utf-8') as f:
            return nbformat.read(f, as_version=4)

    def export_notebook(
        self,
        notebook_path: Union[str, Path],
        output_path: Union[str, Path],
        template: str = "default.j2",
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Export a notebook to the specified format using a Jinja2 template.

        Args:
            notebook_path: Path to the input notebook file.
            output_path: Path where the exported file will be saved.
            template: Name of the template file to use.
            context: Additional context variables for the template.
        """
        # Load the notebook
        notebook = self.load_notebook(notebook_path)

        # Prepare template context
        template_context = {
            'notebook': notebook,
            'metadata': notebook.metadata,
            'cells': notebook.cells,
        }

        if context:
            template_context.update(context)

        # Load and render template
        template_obj = self.env.get_template(template)
        rendered_content = template_obj.render(**template_context)

        # Write output
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)

    def get_available_templates(self) -> list[str]:
        """Get a list of available template files.

        Returns:
            List of template file names.
        """
        if not self.template_dir.exists():
            return []

        templates = []
        for file_path in self.template_dir.glob("*.j2"):
            templates.append(file_path.name)

        return sorted(templates)

    def export_with_config(
        self,
        config_path: Union[str, Path]
    ) -> None:
        """Export notebook(s) using a configuration file.

        Args:
            config_path: Path to YAML configuration file.
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        for export_config in config.get('exports', []):
            self.export_notebook(
                notebook_path=export_config['input'],
                output_path=export_config['output'],
                template=export_config.get('template', 'default.j2'),
                context=export_config.get('context', {})
            )
