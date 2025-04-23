from ep_sdk_4pd.ep_data import EpData


def test_predict_data():
    print('-------------test_predict_data-------------')

    data = EpData.get_predict_data(scope="weather", system_date="2025-04-15")
    print(data)
    print('-------------------------------------')


if __name__ == '__main__':
    test_predict_data()
