import json
import logging
import os

import requests

from ep_sdk_4pd import models as ep_sdk_4pd_models
from datetime import datetime

from ep_sdk_4pd.models import ModelOutputDirRequest, RunStrategyRequest

# test 地址
endpoint = 'http://172.27.88.56:6001'


# prod 地址
# endpoint = 'http://82.157.231.254:6001'

class EpSystem:

    @staticmethod
    def model_output_dir(is_online: bool = False):
        if is_online:
            # 从环境变量中获取策略id
            strategy_id = os.getenv('STRATEGY_ID')
            logging.info(f'strategy_id: {strategy_id}')

            if strategy_id is None:
                raise Exception('STRATEGY_ID is not set')
        else:
            # 线下环境，给固定的策略id
            strategy_id = 63
        request = ModelOutputDirRequest(strategy_id=strategy_id)
        full_url = f'{endpoint}{request.api}'
        headers = {
            'content-type': request.content_type,
        }

        payload = {
            'strategy_id': request.strategy_id
        }

        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
            data=json.dumps(payload),
        )

        base_resp = ep_sdk_4pd_models.BaseResponse(
            code=response.json().get('code', None),
            data=response.json().get('data', None),
            message=response.json().get('message', None),
        )
        response = ep_sdk_4pd_models.ModelOutputDirResponse(response=base_resp)

        if response.code == 200:
            return response.data
        else:
            return None

    @staticmethod
    def get_system_date(is_online: bool = False):
        """
        脚本每次预测的目标日，主要是拦截用户获取越界数据,用户不可修改
        """
        if is_online:
            # 线上环境,随着真实调用运行时间变化
            system_date = datetime.now().strftime('%Y-%m-%d')
        else:
            # 线下环境
            system_date = "2024-12-31"

        return system_date

    @staticmethod
    def get_run_strategy(is_online: bool = False):
        """
        获取此刻运行的策略模型基础信息
        :param is_online:
        :return:
        """
        if is_online:
            # 从环境变量中获取策略id
            strategy_id = os.getenv('STRATEGY_ID')
            logging.info(f'strategy_id: {strategy_id}')

            if strategy_id is None:
                raise Exception('STRATEGY_ID is not set')
        else:
            # 线下环境，给固定的策略id
            strategy_id = 56

        request = RunStrategyRequest(strategy_id=strategy_id)
        full_url = f'{endpoint}{request.api}'
        headers = {
            'content-type': request.content_type,
        }

        payload = {
            'strategy_id': request.strategy_id
        }

        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
            data=json.dumps(payload),
        )

        base_resp = ep_sdk_4pd_models.BaseResponse(
            code=response.json().get('code', None),
            data=response.json().get('data', None),
            message=response.json().get('message', None),
        )
        response = ep_sdk_4pd_models.RunStrategyResponse(response=base_resp)

        if response.code == 200:
            return response.data
        else:
            return None