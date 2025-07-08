# Jupyter Export Template

A Python package that provides Jinja2 templates for exporting Jupyter notebooks to various formats with customizable styling and layouts.

## Features

- 🎨 Customizable Jinja2 templates for notebook export
- 📝 Support for multiple output formats (HTML, PDF, etc.)
- 🔧 Easy-to-use command-line interface
- 📦 Installable as a pip package
- 🧪 Comprehensive test suite
- 📚 Well-documented API

## Installation

### From PyPI (when published)
```bash
pip install jupyter-export-template
```

### From Source
```bash
git clone https://github.com/yourusername/jupyter-export-template.git
cd jupyter-export-template
pip install -e .
```

## Quick Start

### Command Line Usage

Export a notebook using the default template:
```bash
jupyter-export input.ipynb output.html
```

Export with a custom template:
```bash
jupyter-export input.ipynb output.html --template custom_template.j2
```

### Python API Usage

```python
from jupyter_export_template import NotebookExporter

# Create an exporter instance
exporter = NotebookExporter()

# Export notebook to HTML
exporter.export_notebook('input.ipynb', 'output.html')

# Export with custom template
exporter.export_notebook(
    'input.ipynb',
    'output.html',
    template='custom_template.j2'
)
```

## Templates

The package includes several built-in templates:

- `default.j2` - Clean, modern HTML template
- `minimal.j2` - Minimal styling for simple exports
- `academic.j2` - Academic paper-style formatting

### Creating Custom Templates

Templates are standard Jinja2 files that receive a notebook object. Here's a simple example:

```jinja2
<!DOCTYPE html>
<html>
<head>
    <title>{{ notebook.metadata.title or "Notebook Export" }}</title>
    <style>
        /* Your custom CSS here */
    </style>
</head>
<body>
    <h1>{{ notebook.metadata.title or "Exported Notebook" }}</h1>

    {% for cell in notebook.cells %}
        {% if cell.cell_type == 'markdown' %}
            <div class="markdown-cell">
                {{ cell.source | markdown }}
            </div>
        {% elif cell.cell_type == 'code' %}
            <div class="code-cell">
                <pre><code>{{ cell.source }}</code></pre>
                {% if cell.outputs %}
                    <div class="outputs">
                        {% for output in cell.outputs %}
                            {{ output | render_output }}
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
        {% endif %}
    {% endfor %}
</body>
</html>
```

## Development

### Setting up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jupyter-export-template.git
cd jupyter-export-template
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black jupyter_export_template/
flake8 jupyter_export_template/
```

### Type Checking

```bash
mypy jupyter_export_template/
```

## Project Structure

```
jupyter_export_template/
├── jupyter_export_template/     # Main package directory
│   ├── __init__.py             # Package initialization
│   ├── exporter.py             # Main exporter class
│   ├── cli.py                  # Command-line interface
│   ├── filters.py              # Jinja2 custom filters
│   └── templates/              # Built-in templates
│       ├── default.j2
│       ├── minimal.j2
│       └── academic.j2
├── tests/                      # Test suite
├── docs/                       # Documentation
├── examples/                   # Example notebooks and usage
├── setup.py                    # Package setup
├── pyproject.toml             # Modern Python packaging
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Jinja2](https://jinja.palletsprojects.com/) templating engine
- Uses [nbformat](https://nbformat.readthedocs.io/) for notebook processing
- Command-line interface powered by [Click](https://click.palletsprojects.com/)
