import docx2txt
import os
import re
import json
import engines.utils.format_date as format_date
from datetime import datetime
import random

schema = ['姓名', '出生年月', '电话', '性别', '项目名称', '项目责任', '项目时间', '籍贯',
          '政治面貌', '落户市县', '毕业院校', '学位', '毕业时间', '工作时间',
          '工作内容', '职务', '工作单位']


def formate_date_on_json(date_json):
    # 深度优先遍历
    for key in date_json:
        if isinstance(date_json[key], dict):
            formate_date_on_json(date_json[key])
        elif isinstance(date_json[key], list):
            for item in date_json[key]:
                formate_date_on_json(item)
        else:
            # 日期格式转换
            date_json[key] = format_date.convert_dates_accurate_to_the_day(date_json[key])
            # 半角转全角
            date_json[key] = date_json[key].replace(".", "。")
            date_json[key] = date_json[key].replace(",", "，")
            # 去除空格
            date_json[key] = re.sub(r'\s+', '', date_json[key])
            # 去除数字前面的；
            date_json[key] = re.sub(r"；(?=\d)", "", date_json[key])


def test():
    with open('resume_train_20200121/train_data.json', "r", encoding="utf-8") as f1:
        raw_examples = json.loads(f1.read())
        schema_dict = {}
        for line in raw_examples:
            if line == '87af5eb43a78':
                # 解析简历文本内容
                text_content = docx2txt.process(os.path.join('resume_train_20200121/docx', line) + '.docx')
                # 日期格式转换
                text_content = format_date.convert_dates_accurate_to_the_day(text_content)
                text_content = re.sub(r'\n+', '，', text_content)
                text_content = re.sub(r'，+', '，', text_content)
                # 半角转全角
                text_content = text_content.replace(".", "。")
                text_content = text_content.replace(",", "，")
                # 去除空格
                text_content = re.sub(r'\s+', '', text_content)
                # 去除数字前面的；
                text_content = re.sub(r"；(?=\d)", "", text_content)
                print(text_content)
                # 再输出 train_data.json 中的内容
                json_t = raw_examples[line]
                formate_date_on_json(json_t)
                # 格式化json，别凑在一团
                json_t = json.dumps(json_t, indent=4, ensure_ascii=False)
                print(json_t)


def make():
    with open('resume_train_20200121/train_data.json', "r", encoding="utf-8") as f1:
        raw_examples = json.loads(f1.read())
        result_list = []
        for line in raw_examples:
            # if line == '87af5eb43a78':
            # 解析简历文本内容
            text_content = docx2txt.process(os.path.join('resume_train_20200121/docx', line) + '.docx')
            # 日期格式转换
            text_content = format_date.convert_dates_accurate_to_the_day(text_content)
            text_content = re.sub(r'\n+', '，', text_content)
            text_content = re.sub(r'，+', '，', text_content)
            # 半角转全角
            text_content = text_content.replace(".", "。")
            text_content = text_content.replace(",", "，")
            # 去除空格
            text_content = re.sub(r'\s+', '', text_content)
            # 去除数字前面的；
            text_content = re.sub(r"；(?=\d)", "", text_content)
            # print(text_content)
            # 再输出 train_data.json 中的内容
            json_t = raw_examples[line]
            formate_date_on_json(json_t)
            # # 格式化json，别凑在一团
            # json_t = json.dumps(json_t, indent=4, ensure_ascii=False)
            # print(json_t)
            output_list = []

            for item in schema:
                schema_dict = {}

                if item in raw_examples[line] and text_content.find(raw_examples[line][item]) > 0:
                    schema_dict["start_idx"] = text_content.find(raw_examples[line][item])
                    schema_dict["end_idx"] = len(raw_examples[line][item]) + text_content.find(
                        raw_examples[line][item]) - 1
                    schema_dict["type"] = item
                    schema_dict["entity"] = raw_examples[line][item]
                    output_list.append(schema_dict)

                if '项目经历' in raw_examples[line]:
                    for i in range(len(raw_examples[line]['项目经历'])):
                        if item in raw_examples[line]['项目经历'][i] and text_content.find(
                                raw_examples[line]['项目经历'][i][item]) > 0:
                            schema_dict = {}
                            schema_dict["start_idx"] = text_content.find(raw_examples[line]['项目经历'][i][item])
                            schema_dict["end_idx"] = len(
                                raw_examples[line]['项目经历'][i][item]) + text_content.find(
                                raw_examples[line]['项目经历'][i][item]) - 1
                            schema_dict["type"] = item
                            schema_dict["entity"] = raw_examples[line]['项目经历'][i][item]
                            output_list.append(schema_dict)

                if '工作经历' in raw_examples[line]:
                    for i in range(len(raw_examples[line]['工作经历'])):
                        if item in raw_examples[line]['工作经历'][i] and text_content.find(
                                raw_examples[line]['工作经历'][i][item]) > 0:
                            schema_dict = {}
                            schema_dict["start_idx"] = text_content.find(raw_examples[line]['工作经历'][i][item])
                            schema_dict["end_idx"] = len(
                                raw_examples[line]['工作经历'][i][item]) + text_content.find(
                                raw_examples[line]['工作经历'][i][item]) - 1
                            schema_dict["type"] = item
                            schema_dict["entity"] = raw_examples[line]['工作经历'][i][item]
                            output_list.append(schema_dict)

                if '教育经历' in raw_examples[line]:
                    for i in range(len(raw_examples[line]['教育经历'])):
                        if item in raw_examples[line]['教育经历'][i] and text_content.find(
                                raw_examples[line]['教育经历'][i][item]) > 0:
                            schema_dict = {}
                            schema_dict["start_idx"] = text_content.find(raw_examples[line]['教育经历'][i][item])
                            schema_dict["end_idx"] = len(
                                raw_examples[line]['教育经历'][i][item]) + text_content.find(
                                raw_examples[line]['教育经历'][i][item]) - 1
                            schema_dict["type"] = item
                            schema_dict["entity"] = raw_examples[line]['教育经历'][i][item]
                            output_list.append(schema_dict)

            result_dict = {
                "text": text_content,
                "entities": output_list
            }
            result_dict = json.dumps(result_dict, ensure_ascii=False)
            # print(result_dict)
            result_list.append(result_dict)
        # 保存到json文件，加上当前时间
        # 获取当前时间作为文件名的一部分
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = 'resume_train_20200121/' + f'train_date_format_{current_time}.json'
        # 将数据写入JSON文件
        # result_list = repr(result_list).replace('\\', '')
        with open(file_name, 'w') as file:
            json.dump(result_list, file, ensure_ascii=False)
        print('数据写入完成！')


# 切分数据集
def split_data():
    with open('resume_train_20200121/train_data_formatted.json', "r", encoding="utf-8") as f1:
        raw_examples = json.loads(f1.read())
        # 打乱数据
        random.shuffle(raw_examples)
        # 切分数据集
        train_data = raw_examples[:int(len(raw_examples) * 0.85)]
        dev_data = raw_examples[int(len(raw_examples) * 0.85):]
        # test_data = raw_examples[int(len(raw_examples) * 0.9):]
        # 保存到json文件，加上当前时间
        # 获取当前时间作为文件名的一部分
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        train_file_name = 'resume_train_20200121/' + f'train_date_format_{current_time}.json'
        dev_file_name = 'resume_train_20200121/' + f'dev_date_format_{current_time}.json'
        # test_file_name = 'resume_train_20200121/' + f'test_date_format_{current_time}.json'
        # 将数据写入JSON文件
        with open(train_file_name, 'w') as file:
            json.dump(train_data, file, ensure_ascii=False)
        with open(dev_file_name, 'w') as file:
            json.dump(dev_data, file, ensure_ascii=False)
        # with open(test_file_name, 'w') as file:
        #     json.dump(test_data, file, ensure_ascii=False)
        print('分割完成！')


# test()
# make()
split_data()