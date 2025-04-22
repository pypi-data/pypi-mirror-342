
class BaseRequest:
    """
    Model for BaseRequest
    """

    def __init__(self):
        self.api = None
        self.method = None
        self.content_type = None
        self.payload = None


class BaseResponse:
    """
    Model for BaseResponse
    """

    def __init__(
        self, code: int = None, data: dict = None, message: str = None, **kwargs
    ):
        self.code = code
        self.data = data
        self.message = message


class HistoryDataRequest(BaseRequest):
    """
    Model for HistoryDataRequest

    获取具体系统时间往前x天的数据（最晚时间为系统时间 D-2）
    特别注意：get_history_data 或 get_predict_data 会get_system_date进行检测，不可获取system_date以后得数据，避免数据穿越现象
    """

    def __init__(self, scope: str = None, system_date: str = None, days: int = None):
        """
        Args:
            scope: "weather","plant","market"
            system_date: 系统时间
            days: 表示systemDate之前days的数据
        """

        self.scope = scope
        self.system_date = system_date
        self.days = days

        super().__init__()
        self.api = f'/ep/api/sdk/get_history_data'
        self.method = 'POST'
        self.content_type = 'application/json'


class HistoryDataResponse(BaseResponse):
    """
    Model for HistoryDataResponse
    """

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )
