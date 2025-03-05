import json
import os
import glob
import re
from datetime import datetime


def create_post_index(input_dir="posts_json", output_dir="src", output_filename="posts_index.json"):
    """
    Creates a lightweight index of all posts with just the essential information
    needed for the homepage listing.
    """
    index_data = []
    json_files = glob.glob(os.path.join(input_dir, "*.json"))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                filename = os.path.basename(json_file)
                # Extract date and post ID from filename
                match = re.match(r'(\d{4}-\d{2}-\d{2})_(\d+)_', filename)
                if not match:
                    print(f"Could not parse date and ID from filename: {filename}")
                    continue
                
                date_str, post_id = match.groups()
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    print(f"Could not parse date from filename: {filename}")
                    continue
                
                data = json.load(f)
                
                # Extract only the essential information for the index
                post_info = {
                    "id": data["id"],
                    "date": date_str,
                    "filename": filename,
                    "title": ""
                }
                
                # Extract the title from the first block if it exists
                if data["blocks"] and len(data["blocks"]) > 0:
                    first_block = data["blocks"][0]
                    if first_block["type"] == "title" and first_block["chunks"] and len(first_block["chunks"]) > 0:
                        post_info["title"] = first_block["chunks"][0]["zh"]
                
                index_data.append(post_info)
        except Exception as e:
            print(f"Error processing {json_file}: {e}")

    def get_post_date(post):
        try:
            return datetime.strptime(post['date'], "%Y-%m-%d")
        except ValueError:
            return datetime.min

    output_filepath = os.path.join(output_dir, output_filename)
    try:
        sorted_data = sorted(index_data, key=get_post_date)
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        print(f"Created {output_filepath} with lightweight post index.")
    except Exception as e:
        print(f"Error writing to {output_filepath}: {e}")


if __name__ == "__main__":
    create_post_index()
