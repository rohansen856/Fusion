# base image  
FROM python:3.8

# setup environment variable for work directory  
ENV FUSION_HOME=/home/app

# make work directory  
RUN mkdir -p $FUSION_HOME

# set work directory  
WORKDIR $FUSION_HOME

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY requirements.txt $FUSION_HOME

# install dependencies  
RUN pip install --no-cache-dir pip==24.0 && pip install -r requirements.txt

# copy api directory to docker's work directory. 
COPY . $FUSION_HOME

# fix line endings for docker-entrypoint.sh
RUN sed -i 's/\r$//' docker-entrypoint.sh && chmod +x docker-entrypoint.sh

# port where the Django app runs  
EXPOSE 8000

# start server  
CMD ["/bin/bash","docker-entrypoint.sh"]
