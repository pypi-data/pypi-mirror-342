import json

import requests

from ep_sdk_4pd import models as ep_sdk_4pd_models
from ep_sdk_4pd.models import HistoryDataRequest, PredictDataRequest

# test 地址
endpoint = 'http://172.27.88.56:6001'


# prod 地址
# endpoint = 'http://82.157.231.254:6001'

class EpData:

    @staticmethod
    def get_history_data(
            scope,
            system_date,
            days
    ):
        request = HistoryDataRequest(
            scope=scope,
            system_date=system_date,
            days=days,
        )
        response = EpData.history_data(request=request)

        if response.code == 200:
            return response.data
        else:
            return None

    @staticmethod
    def history_data(
            request: ep_sdk_4pd_models.HistoryDataRequest = None,
    ) -> ep_sdk_4pd_models.HistoryDataResponse:

        full_url = f'{endpoint}{request.api}'
        headers = {
            'content-type': request.content_type,
        }

        payload = {
            'scope': request.scope,
            'system_date': request.system_date,
            'days': request.days
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
        return ep_sdk_4pd_models.HistoryDataResponse(response=base_resp)

    @staticmethod
    def get_predict_data(
            scope,
            system_date
    ):
        request = PredictDataRequest(
            scope=scope,
            system_date=system_date,
        )
        response = EpData.predict_data(request=request)

        if response.code == 200:
            return response.data
        else:
            return None

    @staticmethod
    def predict_data(
            request: ep_sdk_4pd_models.PredictDataRequest = None,
    ) -> ep_sdk_4pd_models.PredictDataResponse:

        full_url = f'{endpoint}{request.api}'
        headers = {
            'content-type': request.content_type,
        }

        payload = {
            'scope': request.scope,
            'system_date': request.system_date
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
        return ep_sdk_4pd_models.PredictDataResponse(response=base_resp)