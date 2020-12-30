FROM python:3.6.1-alpine
WORKDIR C:\Users\ADMIN\Documents\GitHub\snakeeyes
EXPOSE 5000
ADD . C:\Users\ADMIN\Documents\GitHub\snakeeyes
COPY requirements.txt /tmp
WORKDIR /tmp
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
RUN pip install -r requirements.txt
WORKDIR C:\Users\ADMIN\Documents\GitHub\snakeeyes
CMD ["flask","app.py"]
