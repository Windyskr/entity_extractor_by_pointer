# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import os
import json
from flask import Flask, request, jsonify
from pprint import pprint
from configure import use_cuda, cuda_device, configure, mode
from engines.data import DataManager
from engines.predict import Predictor
from engines.utils.logger import get_logger
import torch


def fold_check(configures):
    if configures['checkpoints_dir'] == '':
        raise Exception('checkpoints_dir did not set...')

    if not os.path.exists(configures['checkpoints_dir']):
        print('checkpoints fold not found, creating...')
        os.makedirs(configures['checkpoints_dir'])

    if not os.path.exists(configures['checkpoints_dir'] + '/logs'):
        print('log fold not found, creating...')
        os.mkdir(configures['checkpoints_dir'] + '/logs')



if __name__ == '__main__':
    os.environ ['TOKENIZERS_PARALLELISM'] = 'false'
    fold_check (configure)
    logger = get_logger (configure ['checkpoints_dir'] + '/logs')

    if use_cuda:
        if torch.cuda.is_available ():
            if cuda_device == -1:
                device = torch.device ('cuda')
            else:
                device = torch.device (f'cuda:{cuda_device}')
        else:
            raise ValueError (
                "'use_cuda' set to True when cuda is unavailable."
                " Make sure CUDA is available or set use_cuda=False."
            )
    else:
        device = 'cpu'
    logger.info (f'device: {device}')
    data_manager = DataManager (configure, logger = logger)

    # 创建 Flask 应用
    app = Flask (__name__)


    @app.route ('/process_text', methods = ['POST'])
    def process_text ( ):
        try:
            text = request.data.decode ('utf-8')

            # 使用 Predictor 对象进行预测
            predictor = Predictor (configure, data_manager, device, logger)
            result = predictor.predict_one (text)
            print(result)
            return jsonify ({"result": result})
        except Exception as e:
            # 在出现错误时返回一个错误消息
            return jsonify ({"error": str (e)}), 500


    # 启动 Flask 应用
    app.run (host = '127.0.0.1', port = 5555)