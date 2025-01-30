# Build Stage
FROM public.ecr.aws/lambda/python:3.9 as builder
RUN yum install -y gcc python3-devel openssl-devel
WORKDIR /usr/app
COPY requirements.txt .
RUN pip install -r requirements.txt -t ./python/
COPY src ./src

# Final Image
FROM public.ecr.aws/lambda/python:3.9
WORKDIR ${LAMBDA_TASK_ROOT}
COPY --from=builder /usr/app/python/ ./
COPY --from=builder /usr/app/src ./
ENV PYTHONPATH="/var/task:${PYTHONPATH}"
CMD ["main.lambda_handler"]