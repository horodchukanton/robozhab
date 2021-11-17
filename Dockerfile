FROM python:3.10-alpine

RUN mkdir -p /app
WORKDIR '/app'

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -q -r requirements.txt
RUN pip install -q tox

COPY . /app/
RUN pip install -q -e .

CMD ['python3', 'robozhab/main.py']
