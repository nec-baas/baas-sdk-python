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
