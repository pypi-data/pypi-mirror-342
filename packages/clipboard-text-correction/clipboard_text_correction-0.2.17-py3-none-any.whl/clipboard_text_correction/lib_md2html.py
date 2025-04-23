import markdown

def markdown_to_html(md_text):
    """Converte Markdown para HTML garantindo blocos <pre><code> corretamente estilizados"""
    extensions = ['fenced_code']
    md = markdown.Markdown(extensions=extensions, output_format="html5")
    html_content = md.convert(md_text)

    # Adiciona CSS para formatar os blocos de código corretamente
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 10px; }}
            pre {{ background-color: #3b4252; color: #a3be8c; border-radius: 4px; padding: 10px; overflow-x: auto; white-space: pre-wrap; }}
            code {{ font-family: monospace; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    return full_html
