FROM python:3.9

ENV APP_ROOT /data
ADD . ${APP_ROOT}
WORKDIR ${APP_ROOT}

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./
CMD ["python3", "main.py"]