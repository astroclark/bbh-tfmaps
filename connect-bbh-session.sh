#!/bin/bash -x
docker exec -i  -u $(id -u):$(id -g) -t bbh_jupyter_session /bin/bash
