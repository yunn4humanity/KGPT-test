import json

def convert_latest_all_to_en_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        latest_all_data = json.load(f)
    
    en_json_data = []
    
    for entry in latest_all_data:
        en_entry = {
            "id": entry["id"],
            "url": f"https://example.com/sfiles/{entry['id']}",
            "title": entry["labels"]["en"]["value"],
            "text": entry["descriptions"]["en"]["value"]
        }
        en_json_data.append(en_entry)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in en_json_data:
            json.dump(entry, f)
            f.write('\n')

convert_latest_all_to_en_json('latest-all.json', 'en.json')