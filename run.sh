#!/bin/bash

# Set environment variables
export FIRSTNAME=Federico
export LASTNAME=Ferreyra

# Define the Docker image name
image_name="horus_app"

# # Check if the Docker image exists
# if [[ "$(docker images -q $image_name 2> /dev/null)" == "" ]]; then
#     Build the Docker image from the Dockerfile
#     docker build -t $image_name .
# fi

docker build -t $image_name .

# Run the Docker container with the environment variables
docker run -e FIRSTNAME -e LASTNAME -p 8501:8501 $image_name
