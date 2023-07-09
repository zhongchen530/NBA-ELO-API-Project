FROM python:3
ENV PYTHONUNBUFFRED=1
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt
COPY . .

