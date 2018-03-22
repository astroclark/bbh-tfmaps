#!/bin/bash -x
docker run \
    -it -u $(id -u):$(id -g) \
    --rm --name bbh-tf-session \
    -v /home/jclark/Projects/bbh-tfmaps:/bbh-tfmaps \
    -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro \
    -w /bbh-tfmaps -p 8888:8888 jclarkastro/bbh-tfmaps
