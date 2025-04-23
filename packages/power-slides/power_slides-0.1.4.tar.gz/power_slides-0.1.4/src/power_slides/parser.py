import os
import re
import html
import yaml
import importlib.util


def extract_all_configs(markdown_text: str) -> tuple[list, str]:
    config_pattern = re.compile(r"^---\n((?:[^\n]+\n)*?)---\n", re.MULTILINE)
    matches = config_pattern.findall(markdown_text)

    configs = []
    for match in matches:
        try:
            config = yaml.safe_load(match)
            configs.append(config if isinstance(config, dict) else {})
        except yaml.YAMLError:
            configs.append({})

    markdown_without_configs = config_pattern.sub("", markdown_text)

    return configs, markdown_without_configs.strip()


def parse_markdown(markdown_text: str) -> list[str]:
    patterns = {
        "heading": (
            re.compile(r"^(#+)\s+(.+)$", re.MULTILINE),
            lambda m: f"<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>",
        ),
        "bold": (re.compile(r"\*\*(.*?)\*\*"), r"<b>\1</b>"),
        "italic": (re.compile(r"\*(.*?)\*"), r"<i>\1</i>"),
        "blockquote": (
            re.compile(r"^>\s+(.+)$", re.MULTILINE),
            r"<blockquote>\1</blockquote>",
        ),
        "ordered_list": (re.compile(r"^\d+\.\s+(.+)$", re.MULTILINE), r"<li>\1</li>"),
        "unordered_list": (re.compile(r"^-\s+(.+)$", re.MULTILINE), r"<li>\1</li>"),
        "ordered_list": (
            re.compile(r"((?:^\d+\.\s+.+\n?)+)", re.MULTILINE),
            lambda m: f"<ol>"
            + re.sub(r"^\d+\.\s+(.+)$", r"<li>\1</li>", m.group(1), flags=re.MULTILINE)
            + "</ol>",
        ),
        "unordered_list": (
            re.compile(r"((?:^-\s+.+\n?)+)", re.MULTILINE),
            lambda m: f"<ul>"
            + re.sub(r"^-\s+(.+)$", r"<li>\1</li>", m.group(1), flags=re.MULTILINE)
            + "</ul>",
        ),
        "code_block": (
            re.compile(r"```([\s\S]+?)```", re.MULTILINE),
            lambda m: f'<pre class="code-block"><code>{html.escape(m.group(1))}</code></pre>',
        ),
        "inline_code": (
            re.compile(r"`(.+)`"),
            lambda m: f"<code>{html.escape(m.group(1))}</code>",
        ),
        "horizontal_rule": (re.compile(r"^---$", re.MULTILINE), r"<hr>"),
        "image": (re.compile(r"!\[(.*?)\]\((.*?)\)"), r'<img src="\2" alt="\1">'),
        "link": (
            re.compile(r"\[(.*?)\]\((https?:\/\/[^\s)]+)\)"),
            r'<a href="\2" target="_blank">\1</a>',
        ),
        "table_w_head": (
            re.compile(
                r"((?:\| *[^|\r\n]+ *)+\|)(?:\r?\n)((?:\|[ :]?-+[ :]?)+\|)((?:(?:\r?\n)(?:\| *[^|\r\n]+ *)+\|)+)",
                re.MULTILINE,
            ),
            lambda m: "<table><thead><tr>"
            + "".join(
                [f"<th>{cell.strip()}</th>" for cell in m.group(1).split("|")[1:-1]]
            )
            + "</tr></thead><tbody>"
            + "".join(
                [
                    f"<tr>"
                    + "".join(
                        [f"<td>{cell.strip()}</td>" for cell in row.split("|")[1:-1]]
                    )
                    + "</tr>"
                    for row in m.group(3).strip().split("\n")
                ]
            )
            + "</tbody></table>",
        ),
        "table_wo_head": (
            re.compile(
                r"((?:(?:\r?\n)(?:\| *[^|\r\n]+ *)+\|)+)",
                re.MULTILINE,
            ),
            lambda m: "<table><tbody>"
            + "".join(
                [
                    f"<tr>"
                    + "".join(
                        [f"<td>{cell.strip()}</td>" for cell in row.split("|")[1:-1]]
                    )
                    + "</tr>"
                    for row in m.group(1).strip().split("\n")
                ]
            )
            + "</tbody></table>",
        ),
    }

    for _, (pattern, replacement) in patterns.items():
        markdown_text = pattern.sub(replacement, markdown_text)

    return markdown_text.split("<hr>")


def load_layout_function(layout_path):
    spec = importlib.util.spec_from_file_location("layout_module", layout_path)
    layout_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(layout_module)
    return layout_module.apply_layout


def get_slides(markdown_text: str, input_file_path: str) -> list:
    slide_configs, cleaned_markdown = extract_all_configs(markdown_text)
    slide_contents = parse_markdown(cleaned_markdown)

    slides = []
    for i, content in enumerate(slide_contents):
        config = slide_configs[i]

        if "src" in config:
            src_path = config["src"]
            src_absolute_path = os.path.join(os.path.dirname(input_file_path), src_path)

            try:
                with open(src_absolute_path, "r", encoding="utf-8") as f:
                    included_text = f.read()
                included_slides = get_slides(included_text, input_file_path)
                slides.extend(included_slides)
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Included slide file not found: {src_absolute_path}"
                )
            continue

        if "layout" in config:
            layout_path = config["layout"]

            if layout_path.startswith("@"):
                layout_absolute_path = os.path.join(
                    os.path.dirname(__file__), "layouts", layout_path[1:]
                )
            else:
                layout_absolute_path = os.path.join(
                    os.path.dirname(input_file_path), layout_path
                )

            try:
                apply_layout = load_layout_function(layout_absolute_path)
                content = apply_layout(config, content)
            except (FileNotFoundError, AttributeError) as e:
                raise RuntimeError(
                    f"Failed to apply layout from {layout_absolute_path}: {e}"
                )

        slides.append({"config": config, "content": content})

    return slides
