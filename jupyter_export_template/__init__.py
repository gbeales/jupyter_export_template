"""Jupyter Export Template - A Jinja2 template system for exporting Jupyter notebooks."""

from .exporter import NotebookExporter
from .cli import main

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = ["NotebookExporter", "main"]
