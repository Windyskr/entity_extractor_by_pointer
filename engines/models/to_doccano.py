import json

# 从文件中读取数据
with open('resume_train_20200121/raw_data_format_2023-06-12_21-13-03.json', 'r') as file:
    data = json.load(file)

outputs = []

# 处理每个数据并生成输出列表
outputs = []
for item in data:
    output = {
        "text": item["text"],
        "label": []
    }

    for entity in item["entities"]:
        end_idx = entity["end_idx"] + 1  # 增加 1
        output["label"].append([entity["start_idx"], end_idx, entity["type"]])

    outputs.append(output)


# 将输出逐行写入输出文件
with open('output.json', 'w') as file:
    for output in outputs:
        json.dump(output, file, ensure_ascii=False)
        file.write('\n')
