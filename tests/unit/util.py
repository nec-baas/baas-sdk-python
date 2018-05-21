from mock import MagicMock


def mock_service_json_resp(json):
    """
    Service mock を返す。JSON 応答をセットする。

    Args:
        json: Response Json

    Returns:
        mocked service
    """
    response = MagicMock()
    response.json.return_value = json

    service = MagicMock()
    service.execute_rest.return_value = response
    return service


def mock_service_resp(response):
    """
    Service mock を返す。応答をセットする。

    Args:
        response:

    Returns:
        mocked service
    """
    service = MagicMock()
    service.execute_rest.return_value = response
    return service


def get_rest_args(service):
    """
    REST API 呼び出し引数を取得する

    Args:
        service:

    Returns:

    """
    return service.execute_rest.call_args[0]


def get_rest_kwargs(service):
    """
    REST API 呼び出しキーワード引数を取得する

    Args:
        service:

    Returns:

    """
    return service.execute_rest.call_args[1]
