<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Jupyter Export Template Project

This is a Python package for exporting Jupyter notebooks using customizable Jinja2 templates.

## Project Context

- **Main purpose**: Create a pip-installable package that exports Jupyter notebooks to various formats using Jinja2 templates
- **Architecture**: Python package with CLI interface, template engine, and custom filters
- **Key dependencies**: jinja2, nbformat, click, pyyaml

## Code Style Guidelines

- Follow PEP 8 for Python code formatting
- Use type hints for function parameters and return values
- Keep line length to 79 characters maximum
- Use descriptive variable and function names
- Add docstrings to all public functions and classes

## Package Structure

- `jupyter_export_template/` - Main package directory
  - `exporter.py` - Core notebook export functionality
  - `cli.py` - Command-line interface
  - `filters.py` - Custom Jinja2 filters
  - `templates/` - Built-in Jinja2 templates
- `examples/` - Test notebooks and examples
- `tests/` - Unit tests
- `docs/` - Documentation

## Development Guidelines

1. **Templates**: When creating Jinja2 templates, ensure they handle all notebook cell types (markdown, code, raw)
2. **Filters**: Custom filters should be defensive and handle edge cases gracefully
3. **Error handling**: Provide clear error messages for common issues (missing files, invalid templates, etc.)
4. **Testing**: Test with various notebook formats and content types
5. **Documentation**: Update README.md when adding new features or templates

## Template Development

- Templates receive a `notebook` object with `.cells`, `.metadata` properties
- Use custom filters like `markdown`, `render_output`, `format_code` for content processing
- Ensure templates are responsive and handle different screen sizes
- Test templates with notebooks containing various content types (plots, DataFrames, errors, etc.)

## CLI Interface

- Provide intuitive command-line options
- Support both single file and batch processing
- Include helpful error messages and usage examples
- Allow template customization and discovery
