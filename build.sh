#!/usr/bin/env bash

# ./build.sh benetzki 0.0.1 --> benetzki/data-farmer:0.0.1
# ./build.sh benetzki --> benetzki/data-farmer:latest

DOCKER_REPO=$1
DOCKER_TAG=${2-latest}

docker build -f images/Dockerfile.master . -t "$DOCKER_REPO/data-farmer:$DOCKER_TAG"
# docker push "$1/data-farmer:$DOCKER_TAG"
