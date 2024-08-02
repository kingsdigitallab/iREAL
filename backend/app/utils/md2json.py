import re
import json
import argparse
import os
from typing import Dict, Any


def process_directory(input_dir: str, output_dir: str) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".md"):
            input_path = os.path.join(input_dir, filename)
            output_filename = f"{os.path.splitext(filename)[0]}.json"
            output_path = os.path.join(output_dir, output_filename)

            try:
                print(f" - Converting {input_path} to .json...")
                parsed_data = parse_file(input_path)
                save_to_json(parsed_data, output_path)
            except Exception as e:
                print(f" - An error occurred processing {input_path}: {e}")


def parse_file(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")

    content = [remove_line_numbers(line) for line in lines if line.strip()]
    text = " ".join([remove_markdown(line) for line in content])

    parsed_data = {}
    current_section = None
    for line in content:
        if line.startswith("**") or line.startswith("[**"):
            line = line.replace("[", "").replace("]", "")
            line = line.replace("{.underline}", "")
            if ":**" in line:
                current_section, content_start = line.split(":**", 1)
                current_section = remove_markdown(current_section)
                parsed_data[current_section] = [content_start.strip()]
            else:
                current_section = line.strip("*")
                parsed_data[current_section] = []
        elif current_section:
            parsed_data[current_section].append(line)

    parsed_data["text"] = text
    return parsed_data


def remove_line_numbers(line: str) -> str:
    """Remove line numbers."""
    return re.sub(r"^\d+\|", "", line).strip()


def remove_markdown(line: str) -> str:
    """Remove markdown formatting."""
    no_bold = re.sub(r"\*\*", "", line).strip()
    return re.sub(r"\{\..*?\}", "", no_bold).strip()


def save_to_json(parsed_data: Dict[str, Any], output_path: str) -> None:
    try:
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(parsed_data, json_file, indent=4, ensure_ascii=False)
    except IOError as e:
        raise IOError(f"Error writing to file {output_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown files to JSON")
    parser.add_argument(
        "input_dir", help="Path to input directory containing Markdown files"
    )
    parser.add_argument("output_dir", help="Path to output directory for JSON files")
    args = parser.parse_args()

    try:
        process_directory(args.input_dir, args.output_dir)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
