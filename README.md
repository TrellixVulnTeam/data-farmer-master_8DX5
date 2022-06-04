# data-farmer 👨‍🌾

## Requirements

You should have these installed:

- Python 3
- Docker

## Running locally

```shell
# install deps
pip install -r requirements.txt

# start application
python run.py
```

## Running in Docker

```shell
# build the image
## ./build.sh benetzki 0.0.1 --> benetzki/data-farmer:0.0.1
## ./build.sh benetzki --> benetzki/data-farmer:latest
./build.sh DOCKER_REPO DOCKER_TAG

# start the container
## ./run_dev.sh benetzki 0.0.1 {port} --> benetzki/data-farmer:0.0.1, flask on port {port}
## ./run_dev.sh benetzki --> benetzki/data-farmer:latest, flask on port 5555
./run_dev.sh DOCKER_REPO DOCKER_TAG
```