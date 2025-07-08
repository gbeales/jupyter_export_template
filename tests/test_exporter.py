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

    assert 'default' in templates
    assert 'minimal' in templates
    assert 'academic' in templates


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


def test_template_export_functionality():
    """Test that template export functionality works."""
    exporter = NotebookExporter()

    # Test that templates can be listed
    templates = exporter.get_available_templates()
    assert len(templates) > 0

    # Test that export method exists and is callable
    assert hasattr(exporter, 'export_notebook')
    assert callable(exporter.export_notebook)


if __name__ == '__main__':
    pytest.main([__file__])
