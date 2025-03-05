import json
import os
import glob


def merge_json_files(input_dir="posts_json", output_dir="public", output_filename="all_posts.json"):
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
                data = json.load(f)
                merged_data.append(data)
        except Exception as e:
            print(f"Error processing {json_file}: {e}")

    output_filepath = os.path.join(output_dir, output_filename)
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        print(f"Created {output_filepath} with merged JSON data.")
    except Exception as e:
        print(f"Error writing to {output_filepath}: {e}")


if __name__ == "__main__":
    merge_json_files()
