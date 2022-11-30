FROM python:3.8-slim
WORKDIR /opt/python/flask-app
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "./app.py" ]