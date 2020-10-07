#Dockerfile
FROM python:3.8
ADD . /klambda-app
WORKDIR /klambda-app
# Upgrade pip
RUN pip install --upgrade pip
RUN pip install -r /klambda-app/requirements.txt
RUN python /klambda-app/setup.py install
WORKDIR /project

# Serverless 
#RUN apt-get update
#RUN apt-get -y install curl gnupg
#RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
#RUN apt-get -y install nodejs
#RUN npm install -g serverless