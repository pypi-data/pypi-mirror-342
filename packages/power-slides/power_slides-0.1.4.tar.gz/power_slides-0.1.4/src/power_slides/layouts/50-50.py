import re


def apply_layout(config, content):
    pattern = r"(.*):left:\s*(.*?)\s*:right:\s*(.*)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    top_content = match.group(1).strip()
    left_content = match.group(2).strip()
    right_content = match.group(3).strip()

    return f"""
        {top_content}
        <div style="display: flex; justify-content: space-evenly">
            <div>
                {left_content}
            </div>
            <div>
                {right_content}
            </div>
        </div>
    """
