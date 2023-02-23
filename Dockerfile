# syntax=docker/dockerfile:1
# set base image (host OS)
FROM python:3.11

# set the working directory in the container
WORKDIR C:\Users\jamar\Documents\Hobbies\Coding\PvP Bot [Dockerized]

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install --upgrade pip
RUN pip install python-dotenv
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY Source/ .

# command to run on container start
CMD [ "python", "./Bot_Core.py", "--host=0.0.0.0"]