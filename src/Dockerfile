FROM public.ecr.aws/lambda/python:3.10

COPY . .

RUN python3.10 -m pip install poetry && \
  python3.10 -m poetry export --without-hashes --output requirements.txt  && \
  python3.10 -m pip install --root-user-action=ignore -r requirements.txt -t .

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
