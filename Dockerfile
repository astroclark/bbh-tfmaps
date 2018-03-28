FROM ligo/software
LABEL name="BBH-tfmaps" \
      maintainer="James Alexander Clark <james.clark@ligo.org>" \
	  url="https://github.com/astroclark/bbh-tfmaps"
RUN python -m pip install --upgrade setuptools pip \
    && python -m pip install --upgrade jupyter matplotlib \
    && python -m pip install git+https://github.com/ligo-cbc/pycbc@v1.9.0#egg=pycbc
RUN apt-get update && apt-get install -y git dvipng


# Update environment
ENV PYTHONPATH /pyutils:${PYTHONPATH}

# Additional jupyter permissions configuration
RUN mkdir -p -m 777 /jupyter
ENV HOME /jupyter

#CMD jupyter-notebook --ip="*" --no-browser --allow-root
ENTRYPOINT ["/bin/bash"]

