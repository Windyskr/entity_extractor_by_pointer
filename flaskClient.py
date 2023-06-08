# -*- coding: utf-8 -*-
import json
import os

import torch
from flask import Flask, request, jsonify

from configure import use_cuda, cuda_device, configure
from engines.data import DataManager
from engines.utils.logger import get_logger


def fold_check ( configures ):
    if configures ['checkpoints_dir'] == '':
        raise Exception ('checkpoints_dir did not set...')

    if not os.path.exists (configures ['checkpoints_dir']):
        print ('checkpoints fold not found, creating...')
        os.makedirs (configures ['checkpoints_dir'])

    if not os.path.exists (configures ['checkpoints_dir'] + '/logs'):
        print ('log fold not found, creating...')
        os.mkdir (configures ['checkpoints_dir'] + '/logs')


def main ( ):
    # basedir = os.path.abspath (os.path.dirname (__file__))
    os.environ ['TOKENIZERS_PARALLELISM'] = 'false'
    fold_check (configure)
    logger = get_logger (configure ['checkpoints_dir'] + '/logs')
    data_manager = DataManager (configure, logger = None)
    logger.info (json.dumps (configure, indent = 2, ensure_ascii = False))
    logger.info ('mode: predict_one')
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

    from engines.predict import Predictor
    predictor = Predictor (configure, data_manager, device, logger)
    predictor.predict_one('warm up')

    # 创建 Flask 应用
    app = Flask(__name__)

    @app.route('/process_text', methods=['POST'])
    def process_text():
        try:
            sentence = request.data.decode ('utf-8')
            print (sentence)
            result = predictor.predict_one (sentence)
            print (result)
            return jsonify ({"result": result})
        except Exception as e:
            # 在出现错误时返回一个错误消息
            return jsonify ({"error": str (e)}), 500

    # 本地启动 Flask 应用, port5555
    app.run (host = '127.0.0.1', port = 5555, debug = True)

main ()
