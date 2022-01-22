FROM python:3.10.0-slim-buster
WORKDIR /usr/src/app
COPY /requirements.txt ./
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python3" , "./app/app.py" ]