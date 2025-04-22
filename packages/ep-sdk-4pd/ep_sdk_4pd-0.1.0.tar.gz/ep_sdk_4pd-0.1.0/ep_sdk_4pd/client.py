import json

import requests

from ep_sdk_4pd import models as ep_sdk_4pd_models


class Client:
    def __init__(
        self,
        config: ep_sdk_4pd_models.Config,
    ):
        self._endpoint = config.endpoint


    # def __get_endpoint(self) -> None:
    #     # test 地址
    #     self._endpoint = 'http://172.27.88.56:6001'
    #     # prod 地址
    #     # self._endpoint = 'http://82.157.231.254:6001'

    def history_data(
        self,
        request: ep_sdk_4pd_models.HistoryDataRequest = None,
    ) -> ep_sdk_4pd_models.HistoryDataResponse:


        full_url = f'{self._endpoint}{request.api}'
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
