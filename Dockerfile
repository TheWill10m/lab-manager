FROM python:3.12-slim-bullseye

WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ app/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]