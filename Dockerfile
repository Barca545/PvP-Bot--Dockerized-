# syntax=docker/dockerfile:1
#Set base image (host OS)
FROM python:3.11

#Set the working directory in the container
WORKDIR /.

#Copy the dependencies file to the working directory
COPY requirements.txt .

#Install dependencies
RUN pip install --upgrade pip
RUN pip install python-dotenv
RUN pip install -r requirements.txt

#Copy the content of the local src directory to the working directory
COPY src/ .

#Install the path ENVs for credentials and database
ENV PVP_TOKEN="/pvpbot_secrets/Discord_token.json"
ENV DB = "/data/pvpserver.db"

#Command to run on container start
CMD [ "python", "main.py", "--host=0.0.0.0"]