# -*- coding: utf-8 -*-
# @Author : lishouxian
# @Email : gzlishouxian@gmail.com
# @File : predict.py
# @Software: PyCharm
import torch
import os
import time
import json
from torch.utils.data import DataLoader


class Predictor:
    def __init__(self, configs, data_manager, device, logger):
        self.device = device
        self.configs = configs
        self.data_manager = data_manager
        self.logger = logger
        self.checkpoints_dir = configs['checkpoints_dir']
        self.model_name = configs['model_name']
        num_labels = len(self.data_manager.categories)
        if configs['model_type'] == 'bp':
            from engines.models.BinaryPointer import BinaryPointer
            self.model = BinaryPointer(num_labels=num_labels).to(device)
        else:
            from engines.models.GlobalPointer import EffiGlobalPointer
            self.model = EffiGlobalPointer(num_labels=num_labels, device=device).to(device)
        self.model.load_state_dict(torch.load(os.path.join(self.checkpoints_dir, self.model_name)))
        self.model.eval()

    def predict_one(self, sentence):
        """
        预测接口
        """
        start_time = time.time()
        max_len = 512  # 设定滑动窗口的最大长度
        stride = 256  # 设定滑动窗口的步长

        # 将输入句子分割成多个小序列
        tokens = sentence.split(' ')
        windows = [tokens[i:i + max_len] for i in range(0, len(tokens), stride)]

        results_dict = {}

        # 对每个小序列进行预测
        for window in windows:
            window_sentence = ' '.join(window)
            encode_results = self.data_manager.tokenizer(window_sentence, padding=True, truncation=True,
                                                         max_length=max_len)
            input_ids = encode_results.get('input_ids')
            token_ids = torch.unsqueeze(torch.LongTensor(input_ids), 0).to(self.device)
            attention_mask = torch.unsqueeze(torch.LongTensor(encode_results.get('attention_mask')), 0).to(self.device)
            segment_ids = torch.unsqueeze(torch.LongTensor(encode_results.get('token_type_ids')), 0).to(self.device)
            logits, _ = self.model(token_ids, attention_mask, segment_ids)
            logit = torch.squeeze(logits.to('cpu'))

            # 提取当前小序列的预测结果
            window_results = self.data_manager.extract_entities(window_sentence, logit)

            # 合并预测结果
            for class_id, result_set in window_results.items():
                if class_id not in results_dict:
                    results_dict[class_id] = set()
                results_dict[class_id].update(result_set)

        self.logger.info('predict time consumption: %.3f(ms)' % ((time.time() - start_time) * 1000))

        # 将结果从set转换为list
        for class_id in results_dict.keys():
            results_dict[class_id] = list(results_dict[class_id])

        return results_dict

    def predict_test(self):
        test_file = self.configs['test_file']
        if test_file == '' or not os.path.exists(test_file):
            self.logger.info('test dataset does not exist!')
            return
        test_data = json.load(open(test_file, encoding='utf-8'))
        test_loader = DataLoader(
            dataset=test_data,
            batch_size=self.data_manager.batch_size,
            collate_fn=self.data_manager.prepare_data,
        )
        from engines.train import Train
        train = Train(self.configs, self.data_manager, self.device, self.logger)
        train.validate(self.model, test_loader)

    def convert_onnx(self):
        max_sequence_length = self.data_manager.max_sequence_length
        dummy_input = torch.ones([1, max_sequence_length]).to('cpu').long()
        dummy_input = (dummy_input, dummy_input, dummy_input)
        onnx_path = self.checkpoints_dir + '/model.onnx'
        torch.onnx.export(self.model.to('cpu'), dummy_input, f=onnx_path, opset_version=13,
                          input_names=['tokens', 'attentions', 'types'], output_names=['logits', 'probs'],
                          do_constant_folding=False,
                          dynamic_axes={'tokens': {0: 'batch_size'}, 'attentions': {0: 'batch_size'},
                                        'types': {0: 'batch_size'}, 'logits': {0: 'batch_size'},
                                        'probs': {0: 'batch_size'}})

    def show_model_info(self):
        from engines.textpruner import summary
        info = summary(self.model, max_level=3)
        self.logger.info(info)
