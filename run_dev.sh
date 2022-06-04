#!/usr/bin/env bash

# ./run_dev.sh benetzki 0.0.1 {port} --> benetzki/data-farmer:0.0.1, flask on port {port}
# ./run_dev.sh benetzki --> benetzki/data-farmer:latest, flask on port 5555

DOCKER_REPO=$1
DOCKER_TAG=${2-latest}
FLASK_PORT=${3:-5555}

docker run -d \
  -p "$FLASK_PORT:$FLASK_PORT" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  "$DOCKER_REPO/data-farmer:$DOCKER_TAG"
