import os


def apply_config(slides: list) -> list:
    sections = []

    for slide in slides:
        config = slide["config"]
        content = slide["content"]
        classes = " ".join(config.get("classes", []))
        background = config.get("background", "white")
        section = f"""<section class="slide {classes}" style="background: {background}">{content}</section>"""
        sections.append(section)

    return sections


def generate_html(slides: list) -> str:
    html_slides = apply_config(slides)

    base_path = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_path, "presentation_template.html")

    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    return html_template.replace("<!-- $SLIDES$ -->", "\n\n".join(html_slides))
