"""Custom Jinja2 filters for notebook export templates."""

import re
import html
from typing import Any, Dict, List
import markdown


def setup_filters(env) -> None:
    """Set up custom Jinja2 filters for notebook processing.

    Args:
        env: Jinja2 environment to add filters to.
    """
    env.filters['markdown'] = markdown_filter
    env.filters['escape_html'] = escape_html_filter
    env.filters['render_output'] = render_output_filter
    env.filters['format_code'] = format_code_filter
    env.filters['cell_id'] = cell_id_filter


def markdown_filter(text: str) -> str:
    """Convert markdown text to HTML.

    Args:
        text: Markdown text to convert.

    Returns:
        HTML string.
    """
    try:
        import markdown as md
        return md.markdown(text, extensions=['codehilite', 'fenced_code'])
    except ImportError:
        # Fallback to basic HTML escaping if markdown not available
        return html.escape(text).replace('\n', '<br>\n')


def escape_html_filter(text: str) -> str:
    """Escape HTML characters in text.

    Args:
        text: Text to escape.

    Returns:
        HTML-escaped text.
    """
    return html.escape(text)


def render_output_filter(output: Dict[str, Any]) -> str:
    """Render a notebook cell output.

    Args:
        output: Notebook cell output object.

    Returns:
        HTML representation of the output.
    """
    output_type = output.get('output_type', '')

    if output_type == 'stream':
        return f'<pre class="stream-output">{escape_html_filter(output.get("text", ""))}</pre>'

    elif output_type == 'execute_result' or output_type == 'display_data':
        data = output.get('data', {})

        # Handle HTML output
        if 'text/html' in data:
            return f'<div class="output-html">{data["text/html"]}</div>'

        # Handle plain text output
        elif 'text/plain' in data:
            text = data['text/plain']
            if isinstance(text, list):
                text = ''.join(text)
            return f'<pre class="output-text">{escape_html_filter(text)}</pre>'

        # Handle image output
        elif any(key.startswith('image/') for key in data.keys()):
            for mime_type, content in data.items():
                if mime_type.startswith('image/'):
                    return f'<img src="data:{mime_type};base64,{content}" class="output-image" />'

    elif output_type == 'error':
        traceback = output.get('traceback', [])
        error_text = '\n'.join(traceback)
        return f'<pre class="error-output">{escape_html_filter(error_text)}</pre>'

    return '<div class="unknown-output">Unknown output type</div>'


def format_code_filter(code: str, language: str = 'python') -> str:
    """Format code with syntax highlighting.

    Args:
        code: Source code to format.
        language: Programming language for syntax highlighting.

    Returns:
        HTML-formatted code.
    """
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter

        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter(cssclass='highlight')
        return highlight(code, lexer, formatter)
    except ImportError:
        # Fallback without syntax highlighting
        return f'<pre><code class="language-{language}">{escape_html_filter(code)}</code></pre>'


def cell_id_filter(cell: Dict[str, Any]) -> str:
    """Generate a unique ID for a notebook cell.

    Args:
        cell: Notebook cell object.

    Returns:
        Unique cell ID string.
    """
    # Use existing cell ID if available
    if 'id' in cell:
        return str(cell['id'])

    # Generate ID from cell content hash
    import hashlib
    content = str(cell.get('source', ''))
    return f"cell-{hashlib.md5(content.encode()).hexdigest()[:8]}"
