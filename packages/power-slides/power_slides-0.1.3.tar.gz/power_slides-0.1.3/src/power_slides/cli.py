import sys
import os
from power_slides.parser import get_slides
from power_slides.generator import generate_html


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input file>.md [<output dir>]")
        sys.exit(1)

    cwd = os.getcwd()
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    input_file_path = os.path.join(cwd, input_file)
    output_dir_path = os.path.join(cwd, output_dir)

    if not os.path.exists(input_file_path):
        print(f"Error: The file {input_file_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    output_file_path = os.path.join(output_dir_path, "presentation.html")

    print("reading markdown...")
    with open(input_file_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    print("parsing markdown...")
    parsed_slides = get_slides(markdown_text, input_file_path)

    print("generating html...")
    html_output = generate_html(parsed_slides)

    print("writing html...")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"Presentation generated: {output_file_path}")


if __name__ == "__main__":
    main()
