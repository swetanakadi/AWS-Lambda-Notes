
from unittest.mock import Mock, patch

from src.lambda_function import lambda_handler

def test_lambda_handler():
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = "Test response"
        mock_get.return_value.status_code = 200

        e = c = {}
        response = lambda_handler(e, c)

        assert response['status_code'] == 200
        assert response['response_text'] == "Test response"
