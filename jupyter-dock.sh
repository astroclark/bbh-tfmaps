#!/bin/bash -x
docker run \
    -it -u $(id -u):$(id -g) \
    --rm --name bbh_jupyter_session \
    -v /home/jclark/tmp:/work \
    -v /home/jclark/Projects/bbh_timefreq:/bbhmaps \
    -v /home/jclark/Projects/GTwaves:/waves \
    -v ${HOME}/Projects/BNS-bursts/utils:/utils\
    -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro \
    -w /bbhmaps -p 8888:8888 jclarkastro/tfmaps
