# -*- coding: utf-8 -*-
# @Author : Windyskr
# @Email : windyskr@outlook.com
# @File : configure.py
# @Software: PyCharm

# 模式
# train:训练分类器
# interactive_predict:交互模式
# test:跑测试集
# convert2tf:将torch模型保存为tf框架的pb格式文件
# [train, interactive_predict, test, convert2tf]
mode = 'train'

# 使用GPU设备
use_cuda = False
cuda_device = -1

configure = {
    # 训练数据集
    'train_file': 'data/resume_datasets/train_data_1.json',
    # 验证数据集
    'dev_file': 'data/resume_datasets/dev_data_1.json',
    # 没有验证集时，从训练集抽取验证集比例
    'validation_rate': 0.15,
    # 测试数据集
    'test_file': '',
    # 使用的模型
    # bp: binary pointer
    # gp: global pointer
    'model_type': 'bp',
    # 模型保存的文件夹
    'checkpoints_dir': 'checkpoints/resume_datasets',
    # 模型名字
    'model_name': 'best_model.pkl',
    # 类别列表
    'classes': ['姓名', '电话', '性别', '项目责任', '籍贯', '毕业院校', '毕业时间', '工作内容', '出生年月', '项目名称',
                '项目时间', '学位', '工作时间', '工作单位', '职务', '政治面貌', '落户市县'],
    # decision_threshold,binary pointer时需要指定
    'decision_threshold': 0.5,
    # 是否使用苏神的多标签分类的损失函数，默认使用BCELoss
    'use_multilabel_categorical_cross_entropy': True,
    # 使用对抗学习
    'use_gan': False,
    # 目前支持FGM和PGD两种方法
    # fgm:Fast Gradient Method
    # pgd:Projected Gradient Descent
    'gan_method': 'pgd',
    # 对抗次数
    'attack_round': 3,
    # 是否进行warmup
    'warmup': False,
    # warmup方法，可选：linear、cosine
    'scheduler_type': 'linear',
    # warmup步数，-1自动推断为总步数的0.1
    'num_warmup_steps': -1,
    # 句子最大长度
    'max_sequence_length': 512,
    # epoch
    'epoch': 50,
    # batch_size
    'batch_size': 32,
    # dropout rate
    'dropout_rate': 0.5,
    # 每print_per_batch打印损失函数
    'print_per_batch': 100,
    # learning_rate
    'learning_rate': 5e-5,
    # 优化器选择
    'optimizer': 'AdamW',
    # 训练是否提前结束微调
    'is_early_stop': True,
    # 训练阶段的patient
    'patient': 10,
}
