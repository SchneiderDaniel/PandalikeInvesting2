# Use the Python3.7.2 image
FROM python:3.9.2-buster




# Set the working directory to /app
WORKDIR /app

#install python3-dev as well for uwisgi
#RUN apt-get install build-essential python3-dev


# Copy the current directory contents into the container at /app 
ADD . /app

RUN apt-get update
RUN apt-get -y install locales locales-all

RUN pip install --upgrade pip

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]