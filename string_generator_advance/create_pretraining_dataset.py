import json
from sg_advance import generate_sfiles_string, generate_multiple_partial_sfiles

def create_dataset(num_samples, variations_per_sample=5):
    latest_all_data = []
    knowledge_full_data = {}

    # knowledge-full.json 파일 로드
    with open('knowledge-full.json', 'r') as f:
        knowledge = json.load(f)

    for i in range(num_samples):
        full_sfiles = generate_sfiles_string()
        partial_sfiles_list = generate_multiple_partial_sfiles(full_sfiles, variations_per_sample)

        for j, partial_sfiles in enumerate(partial_sfiles_list):
            id = f"Q{i+1}-{j+1}"

            # knowledge-full.json에 있는 엔티티만 사용
            if id not in knowledge:
                continue

            # latest-all.json 형식의 데이터 생성
            latest_all_entry = {
                "id": id,
                "labels": {
                    "en": {
                        "value": full_sfiles
                    }
                },
                "descriptions": {
                    "en": {
                        "value": f"SFILES 2.0 string with partial representation: {partial_sfiles}"
                    }
                },
                "aliases": {
                    "en": [
                        {
                            "value": f"SFILES 2.0 String {i+1} Variation {j+1}"
                        }
                    ]
                },
                "claims": {
                    "P31": [{
                        "mainsnak": {
                            "snaktype": "value",
                            "property": "P31",
                            "datavalue": {
                                "value": {
                                    "entity-type": "item",
                                    "id": "Q123",  # 가정: Q123이 "SFILES 2.0 string"을 나타냄
                                    "numeric-id": 123
                                },
                                "type": "wikibase-entityid"
                            },
                            "datatype": "wikibase-item"
                        },
                        "type": "statement",
                        "rank": "normal"
                    }],
                    "P1": [{
                        "mainsnak": {
                            "snaktype": "value",
                            "property": "P1",
                            "datavalue": {
                                "value": {
                                    "text": full_sfiles,
                                    "language": "en"
                                },
                                "type": "monolingualtext"
                            },
                            "datatype": "monolingualtext"
                        },
                        "type": "statement",
                        "rank": "normal"
                    }],
                    "P2": [{
                        "mainsnak": {
                            "snaktype": "value",
                            "property": "P2",
                            "datavalue": {
                                "value": {
                                    "text": partial_sfiles,
                                    "language": "en"
                                },
                                "type": "monolingualtext"
                            },
                            "datatype": "monolingualtext"
                        },
                        "type": "statement",
                        "rank": "normal"
                    }]
                }
            }

            latest_all_data.append(latest_all_entry)

            # knowledge-full.json 형식의 데이터 생성
            remaining_sfiles = full_sfiles[len(partial_sfiles):]
            if remaining_sfiles.startswith(')'):
                remaining_sfiles = remaining_sfiles[1:]
            knowledge_full_entry = [
                partial_sfiles,
                f"SFILES 2.0 string with partial representation: {partial_sfiles}",
                [["pred", remaining_sfiles]] if remaining_sfiles else []
            ]
            knowledge_full_data[id] = knowledge_full_entry

    return latest_all_data, knowledge_full_data

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 데이터셋 생성 (예: 100개의 샘플, 각 샘플당 5개의 변형)
latest_all, knowledge_full = create_dataset(5, 5)

# JSON 파일로 저장
save_json(latest_all, 'latest-all.json')
save_json(knowledge_full, 'knowledge-full.json')