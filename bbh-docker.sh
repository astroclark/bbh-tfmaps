#!/bin/bash -x
docker run \
    -it -u $(id -u):$(id -g) \
    --rm --name bbh-tf-session \
    -e DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /home/jclark/Projects/bbh-tfmaps:/bbh-tfmaps \
    -v /home/jclark/Projects/bbh-tfmaps/pyutils:/pyutils \
    -v /home/jclark/Projects/lvcnr-lfs/GeorgiaTech:/waves \
    -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro \
    -w /bbh-tfmaps -p 8888:8888 jclarkastro/bbh-tfmaps
