"""Custom nbconvert exporters and templates for Jupyter notebooks."""

import os
from pathlib import Path
from typing import Dict, Any, Optional, Union, List

from nbconvert import HTMLExporter
from traitlets import Unicode, Bool
import yaml

from .filters import setup_filters


class JupyterExportTemplateHTMLExporter(HTMLExporter):
    """Custom HTML exporter that uses our custom templates."""

    # Template file to use
    template_name = Unicode(
        "default",
        help="Name of the template to use (without .j2 extension)"
    ).tag(config=True)

    # Whether to use built-in templates or custom template directory
    use_builtin_templates = Bool(
        True,
        help="Use built-in templates from the package"
    ).tag(config=True)

    # Custom template directory
    custom_template_dir = Unicode(
        "",
        help="Directory containing custom templates"
    ).tag(config=True)

    def __init__(self, **kwargs):
        """Initialize the exporter."""
        # Set template paths and file before parent initialization
        self._setup_template_paths()
        super().__init__(**kwargs)
        self._setup_custom_filters()

    def _setup_template_paths(self):
        """Set up template paths for nbconvert."""
        if self.use_builtin_templates:
            # Use built-in templates
            package_dir = Path(__file__).parent
            template_dir = package_dir / "templates"
            self.template_paths = [str(template_dir)]
        elif self.custom_template_dir:
            # Use custom template directory
            self.template_paths = [self.custom_template_dir]

        # Set the template file for .j2 file templates
        package_dir = Path(__file__).parent
        template_dir = package_dir / "templates"

        # Look for .j2 file template
        j2_template_path = template_dir / f"{self.template_name}.j2"
        if j2_template_path.exists():
            self.template_file = f"{self.template_name}.j2"
        else:
            # Fallback to default template
            self.template_file = "default.j2"

    def _setup_custom_filters(self):
        """Add custom filters to the Jinja2 environment."""
        # Get the environment after parent initialization
        if hasattr(self, 'environment') and self.environment:
            setup_filters(self.environment)

    def from_filename(self, filename, resources=None, **kwargs):
        """Convert a notebook file to HTML."""
        # Ensure filters are set up before conversion
        self._setup_custom_filters()
        return super().from_filename(filename, resources, **kwargs)

    def from_file(self, file_stream, resources=None, **kwargs):
        """Convert a notebook file stream to HTML."""
        # Ensure filters are set up before conversion
        self._setup_custom_filters()
        return super().from_file(file_stream, resources, **kwargs)


class NotebookExporter:
    """Main class for exporting Jupyter notebooks using nbconvert with
    custom templates."""

    def __init__(self, template_dir: Optional[Union[str, Path]] = None):
        """Initialize the notebook exporter.

        Args:
            template_dir: Directory containing Jinja2 templates.
                         If None, uses built-in templates.
        """
        self.template_dir = self._get_template_dir(template_dir)
        self.use_builtin = template_dir is None

    def _get_template_dir(
        self, template_dir: Optional[Union[str, Path]]
    ) -> Path:
        """Get the template directory path."""
        if template_dir is None:
            # Use built-in templates
            package_dir = Path(__file__).parent
            return package_dir / "templates"
        return Path(template_dir)

    def export_notebook(
        self,
        notebook_path: Union[str, Path],
        output_path: Union[str, Path],
        template: str = "default",
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> None:
        """Export a notebook to HTML using nbconvert with custom template.

        Args:
            notebook_path: Path to the input notebook file.
            output_path: Path where the exported file will be saved.
            template: Name of the template to use.
            context: Additional context variables for the template.
            **kwargs: Additional arguments passed to the exporter.
        """
        # Remove .j2 extension if present
        if template.endswith('.j2'):
            template = template[:-3]

        # Use simple HTMLExporter approach
        from nbconvert import HTMLExporter
        exporter = HTMLExporter()

        # Set template file and paths
        exporter.template_file = f"{template}.j2"
        exporter.template_paths = [str(self.template_dir)]

        # Add custom filters if needed
        try:
            setup_filters(exporter.environment)
        except Exception:
            # Continue without filters if they fail
            pass

        # Add any additional context as resources
        resources = context or {}

        # Convert the notebook
        (body, resources) = exporter.from_filename(
            str(notebook_path), resources=resources
        )

        # Write output
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(body)

    def get_available_templates(self) -> List[str]:
        """Get a list of available template files.

        Returns:
            List of template file names (without .j2 extension).
        """
        if not self.template_dir.exists():
            return []

        templates = set()  # Use set to avoid duplicates

        # Check for .j2 files (legacy format)
        for file_path in self.template_dir.glob("*.j2"):
            template_name = file_path.stem
            templates.add(template_name)

        # Check for template directories (nbconvert format)
        for dir_path in self.template_dir.iterdir():
            if dir_path.is_dir() and (dir_path / "index.html.j2").exists():
                template_name = dir_path.name
                if template_name.startswith('custom-'):
                    # Remove 'custom-' prefix for user-friendly names
                    template_name = template_name[7:]
                templates.add(template_name)

        return sorted(list(templates))

    def export_with_config(self, config_path: Union[str, Path]) -> None:
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
                template=export_config.get('template', 'default'),
                context=export_config.get('context', {})
            )

    def list_nbconvert_templates(self) -> List[str]:
        """List all available nbconvert templates (built-in and custom).

        Returns:
            List of available template names.
        """
        # Get our custom templates
        custom_templates = [
            f"custom.{t}" for t in self.get_available_templates()
        ]

        return sorted(custom_templates)


def register_template_path():
    """Register our template directory with nbconvert."""
    package_dir = Path(__file__).parent
    template_dir = package_dir / "templates"

    # Add our template directory to nbconvert's search path
    if 'JUPYTER_PATH' in os.environ:
        os.environ['JUPYTER_PATH'] += os.pathsep + str(template_dir)
    else:
        os.environ['JUPYTER_PATH'] = str(template_dir)


# Register templates when module is imported
register_template_path()
