import json

def save_to_json(data, output_path):
    """Saves a dictionary directly to a JSON file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully created {output_path}")
    except Exception as e:
        print(f"Error saving JSON file to {output_path}: {e}")