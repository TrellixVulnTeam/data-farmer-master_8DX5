# ./build.sh 0.0.1 --> kraleppa/data-farmer-master:0.0.1
# ./build.sh --> kraleppa/data-farmer-master:latest

docker build . -t kraleppa/data-farmer-master:${1:-latest}
docker push kraleppa/data-farmer-master:${1:-latest}
