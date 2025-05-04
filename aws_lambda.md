# AWS Lambda

### What is it?
Serverless compute service that runs your code in response to events without requiring to provision servers

### Why lambda?
- Automatic scaling
- Pay-per-use pricing
- No server management required
- Native integration with AWS services

### Runtime Environment Details
- Provides linux environment
- Each function runs in an isolated environment with its own allocated memory and CPU
- Maximum execution duration: 15 minutes
- Memory allocation: 128MB to 10GB
- Temporary disk space: 512MB to 10GB

### Lambda function structure
```
    def lambda_function(event, context):
        # your code here

```
- event (object): contains input data for lambda function. Its mostly in JSON format i.e. python dict. However, other datatypes of python such as list, str, int, float are also supported.
- context (object): provides runtime information like function_name, function_version, memory_limit_in_mb, aws_request_id, log_group_name, log_stream_name, remaining_time_in_millis, etc


### Dockerizing lambda
```commandline
Build container: docker build -t aws-lambda .

Run container: docker run -p 8080:8080 aws-lambda
```


### Simulating call to lambda-function
```
curl -XPOST "http://localhost:8080/2015-03-31/functions/function/invocations"   -d '{"e": "value", "c": ""}'

where:
- /2015-03-31/ = fixed API version identifier
- functions/function/invocations = standard local Lambda runtime endpoint
- -d = used to specify event and context as JSON format
```


### Using AWS lambda with S3 and localstack for testing
* Install localstack and aws cli
  * mkdir -p ~/localstack && cd ~/localstack
  * python3 -m venv venv
  * source venv/bin/activate
  * pip install --upgrade localstack

* Start localstack
  * localstack start
  * docker run --rm -it --name localstack --network=lambda-localstack -p 4566:4566 localstack/localstack(optionally create a docker network, attach localstack in this network where you have to use other aws containerized services e.g. aws lambda's docker network)

* Install aws cli
  * pip install --upgrade --user awscli
  
* Configure aws-cli with dummy creddentials
  * aws configure
    ```AWS Access Key ID [None]: AKIADUMMY           
    AWS Secret Access Key [None]: 9P4YqgQsZTest
    Default region name [None]: us-east-1
    Default output format [None]: ```
  
* Check s3 buckets using
   * aws --endpoint-url=http://localhost:4566 s3 ls
  
* Make s3 bucket using
  * aws --endpoint-url=http://localhost:4566 s3 mb s3://test-bucket

* Upload to test bucket using
  * aws --endpoint-url=http://localhost:4566 s3 cp PULRETEST-202412-990\ 2023-11272024990\(1\).pdf s3://test-bucket/

* Download from s3 bucket to localhost:
  * aws --endpoint-url=http://localhost:4566 s3 cp s3://test-bucket/#1305180005-1304155929_XML-20250306122604.xml ./processed_xml_file.xml

### Test localstack with required AWS service, here its aws lambda

* Build docker image
    ```
    docker build -f Dockerfile-lambda -t tege_lambda .  
    ```
* Run image
  ```
    docker run -p 8080:8080 --network=lambda-localstack --name tege_lambda --rm tege_lambda
  ```
    
* Create a lambda event for uploaded file
```
{
  "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "2023-03-05T12:34:56.789Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklm"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "test-bucket",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::test-bucket"
        },
        "object": {
          "key": "1304155929_XML-2022-990-202209-0919502244.xml",
          "size": 1024,
          "eTag": "d41d8cd98f00b204e9800998ecf8427e",
          "sequencer": "0055AED6DCD90281E5"
        }
      }
    }
  ]
}

```

* Invoke lambda with the dummy event
  ```
  curl -XPOST "http://localhost:8080/2015-03-31/functions/function/invocations" -d @event.json
  ```
  


  