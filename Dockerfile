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

#Install the path ENVs for credentials 
ENV GOOGLE_APPLICATION_CREDENTIALS="/working/pvpbot_secrets/v2-bot-374602-e64743327d13.json"
ENV PVP_TOKEN="/working/pvpbot_secrets/Discord_token.json"

#Command to run on container start
CMD [ "python", "main.py", "--host=0.0.0.0"]