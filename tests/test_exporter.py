"""Basic tests for jupyter-export-template package."""

import tempfile
import pytest
from pathlib import Path
from jupyter_export_template import NotebookExporter


def test_exporter_initialization():
    """Test that the exporter can be initialized."""
    exporter = NotebookExporter()
    assert exporter is not None


def test_get_available_templates():
    """Test that built-in templates are available."""
    exporter = NotebookExporter()
    templates = exporter.get_available_templates()

    assert 'default.j2' in templates
    assert 'minimal.j2' in templates
    assert 'academic.j2' in templates


def test_export_notebook_basic():
    """Test basic notebook export functionality."""
    # This would require a test notebook file
    # For now, just test that the method exists
    exporter = NotebookExporter()
    assert hasattr(exporter, 'export_notebook')


def test_template_directory_setup():
    """Test that template directory is properly set up."""
    exporter = NotebookExporter()
    assert exporter.template_dir.exists()
    assert exporter.template_dir.is_dir()


def test_jinja_environment():
    """Test that Jinja2 environment is properly configured."""
    exporter = NotebookExporter()
    assert exporter.env is not None

    # Test that custom filters are installed
    assert 'markdown' in exporter.env.filters
    assert 'render_output' in exporter.env.filters
    assert 'format_code' in exporter.env.filters
    assert 'cell_id' in exporter.env.filters


if __name__ == '__main__':
    pytest.main([__file__])
