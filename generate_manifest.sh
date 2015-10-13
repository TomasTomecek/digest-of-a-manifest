set -ex
cat >Dockerfile <<EOF
FROM busybox
MAINTAINER ľščťť <mail@example.com> "asd & qwe"
LABEL asdqwe="asd +ľššč < qwe > &"
RUN ls -lha / >/qwe &>zxcasd
EOF
docker build --tag=e .

docker pull registry:2
docker run --net=host --name=reg -d registry:2
docker tag e localhost:5000/e
sleep 2  # registry may still not be running
docker push localhost:5000/e
curl -s http://localhost:5000/v2/e/manifests/latest >manifest.json
docker stop reg
docker rm reg
docker rmi -f localhost:5000/e e
rm Dockerfile
