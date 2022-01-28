FROM python:3.10-alpine

RUN mkdir -p /app
WORKDIR '/app'

COPY requirements.txt /app/
RUN pip install --no-cache-dir -q -r requirements.txt

COPY ./ /app/
RUN pip install -q -e .

CMD 'robozhab'
