FROM public.ecr.aws/lambda/python:3.8

# this is /var/task location in the container
WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

# install requirements
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# copy source code
COPY /src .

# start lambda function
CMD ["lambda_function.lambda_handler"]