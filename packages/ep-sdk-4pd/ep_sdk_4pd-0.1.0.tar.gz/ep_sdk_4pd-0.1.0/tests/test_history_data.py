import ep_sdk_4pd.client as ep_sdk_4pd_client
import ep_sdk_4pd.models as ep_sdk_4pd_models


def test_history_data():
    print('-------------test client-------------')

    config = ep_sdk_4pd_models.Config()
    client = ep_sdk_4pd_client.Client(config=config)
    request = ep_sdk_4pd_models.HistoryDataRequest(
        scope="weather",
        system_date="2025-04-17",
        days=2,
    )
    response = client.history_data(request=request)
    print(response.code)
    print(response.data)
    print(response.message)
    print('-------------------------------------')


if __name__ == '__main__':
    test_history_data()
