import json
import os
import glob
import re
import html


def extract_date_from_filename(filename):
    """
    Extracts the date string from a filename with the format "posts/YYYY-MM-DD_HHMMSS_...".

    Args:
      filename: The filename string.

    Returns:
      The date string in YYYY-MM-DD format, or None if no date is found.
    """
    match = re.search(r"(\d{4}-\d{2}-\d{2})",
                      filename)  # Use regex to find the date pattern

    if match:
        return match.group(1)  # Return the first captured group (the date)
    else:
        return None  # Return None if no date is found


def sanitize_html_content(content):
    """
    Sanitizes HTML content to prevent XSS attacks by escaping HTML special characters.
    """
    return html.escape(content)


def create_html_from_json(json_file, output_dir="html_output"):
    """
    Reads a JSON file, extracts data, and creates a corresponding HTML file.
    Returns data needed for index.html or None if error occurs.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: File not found: {json_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file: {json_file}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading {json_file}: {e}")
        return None

    date_string = extract_date_from_filename(json_file)
    if not date_string:
        print(f"Error: Could not extract date from filename: {json_file}")
        return None

    try:
        post_id = data['id']
        title_zh = data['title_zh']
        title_en = data['title_en']
        content_zh = data['content_zh']
        content_en = data['content_en']
        replies = data['replies']
    except KeyError as e:
        print(f"Error: Missing key {e} in JSON: {json_file}")
        return None
    except TypeError as e:
        # More specific error message
        print(f"Error: Data type mismatch in JSON: {json_file} - {e}")
        return None
    except Exception as e:
        print(
            f"An unexpected error occurred while processing data from {json_file}: {e}")
        return None

    sanitized_title_en = sanitize_html_content(title_en)
    sanitized_title_zh = sanitize_html_content(title_zh)
    sanitized_content_en = sanitize_html_content(content_en)
    sanitized_content_zh = sanitize_html_content(content_zh)

    sanitized_replies_list = []
    for reply in replies:
        sanitized_replies_list.append({
            "en": sanitize_html_content(reply["en"]),
            "zh": sanitize_html_content(reply["zh"])
        })

    html_content = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sanitized_title_en}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>{sanitized_title_en}</h1>
        <details>
            <summary>Show Chinese Title</summary>
            <h3>{sanitized_title_zh}</h3>
        </details>
        <div class="content">
            <p>{sanitized_content_en}</p>
            <details>
                <summary>Show Chinese Content</summary>
                <p>{sanitized_content_zh}</p>
            </details>
        </div>
        <div class="replies">
            <ul>
                {''.join([f'<li>{reply["en"]}<br><details><summary>Show Chinese Reply</summary>{reply["zh"]}</details></li>' for reply in sanitized_replies_list])}
            </ul>
        </div>
    </div>
</body>
</html>
"""

    output_file = os.path.join(
        output_dir, f"post_{date_string}_{post_id}.html")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Created {output_file}")
        # Return data for index
        return {"html_file": os.path.basename(output_file), "title_en": title_en, "title_zh": title_zh}
    except Exception as e:
        print(f"Error writing to file {output_file}: {e}")
        return None


def create_index_html(index_data, output_dir="html_output"):
    """Creates an index.html file to list all the post HTML files.
       Now accepts pre-processed index_data.
    """

    list_items = []
    for item in index_data:
        html_file = item['html_file']
        sanitized_title_index = sanitize_html_content(item['title_zh'])
        id = html_file.removeprefix('post_').removesuffix('.html')
        list_items.append(
            f'<li>[{id}]<a href="{html_file}">{sanitized_title_index}</a></li>')

    index_content = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Posts</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>list:</h1>
        <ul>
            {''.join(list_items)}
        </ul>
    </div>
</body>
</html>
"""

    index_file = os.path.join(output_dir, "index.html")
    try:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"Created {index_file}")
    except Exception as e:
        print(f"Error writing to file {index_file}: {e}")


def process_all_json_files(directory="posts", output_dir="html_output", file_pattern="*translated.json"):
    """
    Processes JSON files, creates HTML, and then index.html using collected data.
    """
    json_files = glob.glob(os.path.join(directory, file_pattern))
    if not json_files:
        print(
            f"No files matching pattern '{file_pattern}' found in directory: {directory}")
        return

    # Sort the json_files list alphabetically by filename
    json_files.sort()

    index_data = []  # Collect data for index.html
    for json_file in json_files:
        item_data = create_html_from_json(
            json_file, output_dir)  # Get data back
        if item_data:  # Only add if create_html_from_json was successful
            index_data.append(item_data)

    create_index_html(index_data, output_dir)  # Pass collected data


process_all_json_files(
    file_pattern="*translate.json")  # Uses a different pattern
