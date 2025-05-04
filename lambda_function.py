import requests

def lambda_handler(event, context):
    try:
        url = "https://api.github.com/zen"
        response = requests.get(url)

        result =  {
            'url': url,
            'response_text': response.text,
            'status_code': 200
        }
        print(result)
        return result
    except Exception as e:
        return {
            'response_text': str(e),
            'status_code': 400
        }


if __name__ == "__main__":
    event = context = {}
    lambda_handler(event, context)