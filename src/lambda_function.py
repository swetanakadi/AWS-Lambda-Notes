import requests
import json

from PIL import Image

# EXAMPLE 1
# A lambda function just to handle API request and process it
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

# EXAMPLE 2
# An event based lambda function
"""
(In this case it is triggered on S3 CreateObject Event)
1. Triggered when a file is uploaded on S3
2. Downloads it and applies some kind of processing
3. Saves processed file again on S3 (can upload on same source bucket(if same source bucket don't fall in the trap of infinite function call!!!!!) or different bucket)
"""

s3_client = boto3.client('s3',)

def lambda_handler(event, context):
    print('event', event)
    print('context', context)

    # Assuming the S3 event sends bucket name and object key in below format
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    # Avoid processing if the object is stored with #
    if object_key.startswith("#"):
        print("File already processed %s", object_key)
        return


    download_path = '/tmp/' + os.path.basename(object_key)
    s3_client.download_file(bucket_name, object_key, download_path)
    print("File %s downloaded at %s", object_key, download_path)

    # modify file and upload in processed folder of s3 bucket
    with open(download_path, 'r') as reader:
        file_content = reader.read()
    modified_content = file_content.upper()
    print('modified_content', modified_content)

    # upload modified content again in S3 in processed file
    upload_key = f"#{os.path.basename(object_key)}"
    with open(download_path, 'w') as file:
        file.write(modified_content)

    s3_client.upload_file(download_path, bucket_name, upload_key)

    return {
        "status_code": 200,
        'body': f"File processed and saved to {upload_key}"
    }


# EXAMPLE 3
# Lambda function that handles specific task - Needs explicit fucntion call unlike a lambda triggered on event
def lambda_handler(event, context):
    # function to extract data and store in S3
    uploaded_image_key = event["s3_key"]
    print("Image uploaded on S3's path: %s", uploaded_image_key)

    try:
        s3_response = s3_client.get_object(Bucket=BUCKET, Key=uploaded_image_key)
        image_binary_content = s3_response["Body"].read()
        
        # Load image from bytes
        image = Image.open(io.BytesIO(image_binary_content))
        # Run processing on the downloaded content of image
        pass

        # Again save processed image in S3
        upload_key = f"processed_{uploaded_image_key}"

        response = s3_client.put_object(Body=prcessed_image_binary, Bucket=BUCKET, Key=upload_key)     
    except Exception as e:
        logger.info("Error in Tesseract processing: %s", str(e))
        return None


if __name__ == "__main__":
    event = context = {}
    lambda_handler(event, context)

    lambda_client = boto3.client(
    'lambda',
    region_name=REGION
    )

    # For example 3, lambda function should be invoked as:
     payload = {
             "s3_key": upload_key      # this will be the input to lambda function i.e. the "event" parameter
            }
    lambda_client.invoke(FunctionName=function_name,      # function name set in aws
                                 InvocationType="Event",  # event for asynchronous call i.e. calling function won't wait until lambda function has completed its entire execution
                                 Payload=json.dumps(payload))

# NOTE: For Synchronous type call of lambda function use InvocationType as "RequestResponse"

