#Dockerfile
FROM python:3.8
ADD . /klambda-app
WORKDIR /klambda-app
# Upgrade pip
RUN pip install --upgrade pip
RUN pip install -r /klambda-app/requirements.txt
RUN python /klambda-app/setup.py install
WORKDIR /project
ENTRYPOINT [ "klambda" ]