# FROM python:3.11.2-bullseye

FROM python:3.11.2-slim


#
WORKDIR /myapp
COPY ./requirements.txt /myapp/requirements.txt


RUN pip install --no-cache-dir -r requirements.txt

COPY ./main.py /myapp/main.py


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]