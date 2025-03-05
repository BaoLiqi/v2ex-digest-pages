import json
import os
import glob
import re
from datetime import datetime


def merge_json_files(input_dir="posts_json", output_dir="src", output_filename="all_posts.json"):
    """
    Merges all JSON files from input_dir into a single JSON array
    and saves it to output_dir/output_filename.
    """
    merged_data = []
    json_files = glob.glob(os.path.join(input_dir, "*.json"))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                filename = os.path.basename(json_file)
                date_str = filename.split('_')[0]
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    print(f"Could not parse date from filename: {filename}")
                    continue
                data = json.load(f)
                data['filename'] = filename  # Add filename to data
                merged_data.append(data)
        except Exception as e:
            print(f"Error processing {json_file}: {e}")

    def get_post_date(post):
        filename = post['filename']
        date_str = filename.split('_')[0]
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return datetime.min  # Ensure posts with invalid dates are at the beginning

    output_filepath = os.path.join(output_dir, output_filename)
    try:
        sorted_data = sorted(merged_data, key=get_post_date)
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        print(f"Created {output_filepath} with merged and sorted JSON data.")
    except Exception as e:
        print(f"Error writing to {output_filepath}: {e}")


if __name__ == "__main__":
    merge_json_files()
