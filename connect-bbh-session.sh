#!/bin/bash -x
docker exec -i  -u $(id -u):$(id -g) -t bbh-tf-session /bin/bash
