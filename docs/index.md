# Documentation

Welcome to the jupyter-export-template documentation!

## Getting Started

### Installation

```bash
pip install jupyter-export-template
```

### Quick Start

```bash
# Export with default template
jupyter-export notebook.ipynb output.html

# List available templates
jupyter-export --list-templates

# Use a specific template
jupyter-export notebook.ipynb output.html --template minimal.j2
```

## API Reference

### NotebookExporter Class

Main class for exporting notebooks:

```python
from jupyter_export_template import NotebookExporter

exporter = NotebookExporter()
exporter.export_notebook('input.ipynb', 'output.html')
```

### Command Line Interface

The package provides the `jupyter-export` command with the following options:

- `--template, -t`: Specify template file
- `--template-dir`: Custom template directory
- `--config, -c`: Configuration file for batch export
- `--list-templates`: List available templates

## Template Development

### Template Structure

Templates are Jinja2 files that receive:
- `notebook`: The notebook object
- `cells`: List of notebook cells
- `metadata`: Notebook metadata

### Custom Filters

Available filters:
- `markdown`: Convert markdown to HTML
- `render_output`: Render cell output
- `format_code`: Format code with syntax highlighting
- `cell_id`: Generate unique cell IDs

### Example Template

```jinja2
<!DOCTYPE html>
<html>
<head>
    <title>{{ notebook.metadata.title or "Notebook" }}</title>
</head>
<body>
    {% for cell in notebook.cells %}
        {% if cell.cell_type == 'markdown' %}
            <div class="markdown-cell">
                {{ cell.source | markdown | safe }}
            </div>
        {% elif cell.cell_type == 'code' %}
            <div class="code-cell">
                <pre><code>{{ cell.source }}</code></pre>
                {% for output in cell.outputs %}
                    {{ output | render_output | safe }}
                {% endfor %}
            </div>
        {% endif %}
    {% endfor %}
</body>
</html>
```

## Configuration Files

Use YAML configuration for batch processing:

```yaml
exports:
  - input: "notebook1.ipynb"
    output: "output1.html"
    template: "default.j2"
  - input: "notebook2.ipynb"
    output: "output2.html"
    template: "academic.j2"
```
