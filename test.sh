#!/bin/bash
### CONFIG ###

workers=1 # Number of web servers workers
n=1000 # Apache2 bench: Requests count per test
c=10 # Apache2 bench: Concurrency requests
r=3 # Repeat count number

##############

docker stop fastapi_098 >/dev/null 2>&1
docker rm fastapi_098 >/dev/null 2>&1

docker stop fastapi_100 >/dev/null 2>&1
docker rm fastapi_100 >/dev/null 2>&1

echo "Build...."
docker build -t fastapi_098-test -f app098/Dockerfile .>/dev/null 2>&1
docker build -t fastapi_100-test -f app100/Dockerfile .>/dev/null 2>&1

docker build -t apache2_ab -f Dockerfile_test_client .>/dev/null 2>&1

echo "Testing fastapi_098..."
docker compose up -d fastapi_test_db fastapi_098 >/dev/null 2>&1

fastapi_098_mu=$(docker stats fastapi_098 --no-stream --format "{{.MemUsage}}" | cut -d '/' -f 1)

echo "Run ${n} Requests per iteration with concurrency ${c}...."
printf "before requests %15s\n" $fastapi_098_mu
printf "requests/second WRITE   %13s \n" "fastapi_098"
for i in $(seq 1 $r)
do
    sleep 0.2
    fastapi_098_rs_l=$(docker run --network=fastapi_test apache2_ab sh -c "ab -q -p test_post.json -T application/json -c 10 -n 1000 http://fastapi_098:8000/posts | grep 'Requests per second' | tr -dc '0-9.0-9'")
    printf "#%s              %15s\n" $i $fastapi_098_rs_l

done

printf "requests/second READ DB  %14s \n" "fastapi_098"
for i in $(seq 1 $r)
do
    sleep 0.2
    fastapi_098_rs_l=$(docker run --network=fastapi_test apache2_ab sh -c "ab -q -n ${n} -c ${c} http://fastapi_098:8000/posts?per_page=100 | grep 'Requests per second' | tr -dc '0-9.0-9'")
    printf "#%s              %15s\n" $i $fastapi_098_rs_l

done

printf "requests/second READ synthetic  %14s \n" "fastapi_098"
for i in $(seq 1 $r)
do
    sleep 0.2
    fastapi_098_rs_l=$(docker run --network=fastapi_test apache2_ab sh -c "ab -q -n ${n} -c ${c} http://fastapi_098:8000/posts_synthetic?per_page=100 | grep 'Requests per second' | tr -dc '0-9.0-9'")
    printf "#%s              %15s\n" $i $fastapi_098_rs_l

done

echo "sleeping 1"
sleep 1
fastapi_098_mu=$(docker stats fastapi_098 --no-stream --format "{{.MemUsage}}" | cut -d '/' -f 1)
printf "after requests %15s\n" $fastapi_098_mu
# #####################################################
echo "Cleaning before another test..."
docker compose down -v >/dev/null 2>&1
# #####################################################

echo "Testing fastapi_100..."
docker compose up -d fastapi_test_db fastapi_100 >/dev/null 2>&1

fastapi_100_mu=$(docker stats fastapi_100 --no-stream --format "{{.MemUsage}}" | cut -d '/' -f 1)

echo "Run ${n} Requests per iteration with concurrency ${c}...."
printf "before requests %15s\n" $fastapi_100_mu
printf "requests/second WRITE   %13s \n" "fastapi_100"
for i in $(seq 1 $r)
do
    sleep 0.2
    fastapi_100_rs_l=$(docker run --network=fastapi_test apache2_ab sh -c "ab -q -p test_post.json -T application/json -c 10 -n 1000 http://fastapi_100:8000/posts | grep 'Requests per second' | tr -dc '0-9.0-9'")
    printf "#%s              %15s\n" $i $fastapi_100_rs_l

done

printf "requests/second READ   %14s \n" "fastapi_100"
for i in $(seq 1 $r)
do
    sleep 0.2
    fastapi_100_rs_l=$(docker run --network=fastapi_test apache2_ab sh -c "ab -q -n ${n} -c ${c} http://fastapi_100:8000/posts?per_page=100 | grep 'Requests per second' | tr -dc '0-9.0-9'")
    printf "#%s              %15s\n" $i $fastapi_100_rs_l

done

printf "requests/second READ synthetic  %14s \n" "fastapi_098"
for i in $(seq 1 $r)
do
    sleep 0.2
    fastapi_100_rs_l=$(docker run --network=fastapi_test apache2_ab sh -c "ab -q -n ${n} -c ${c} http://fastapi_100:8000/posts_synthetic?per_page=100 | grep 'Requests per second' | tr -dc '0-9.0-9'")
    printf "#%s              %15s\n" $i $fastapi_100_rs_l

done

echo "sleeping 1"
sleep 1
fastapi_100_mu=$(docker stats fastapi_100 --no-stream --format "{{.MemUsage}}" | cut -d '/' -f 1)
printf "after requests %15s\n" $fastapi_100_mu

echo "Cleanup...."
docker compose down -v >/dev/null 2>&1