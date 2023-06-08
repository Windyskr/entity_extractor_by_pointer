import json

# 读取JSON文件
with open('train_data.json', 'r') as file:
    data = json.load(file)

# 遍历每个对象，将end_idx减1
for obj in data:
    if 'entities' in obj:
        for entity in obj['entities']:
            entity['end_idx'] -= 1

# 保存修改后的JSON文件
with open('train_data_1.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)