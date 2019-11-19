FROM nvidia/cuda:9.0-cudnn7-devel

# Basic env setup
COPY . /opt
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Install arterys library
RUN apt-get update && apt-get install -y git curl

# Install Conda
RUN curl --location --remote-name http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda
RUN conda install python=3.6 -y

RUN pip install git+https://github.com/fepegar/arterys#egg=arterys
RUN pip install torch==1.3.1+cu92 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install highresnet==0.10.0

EXPOSE 8000
ENTRYPOINT ["/miniconda/bin/python", "/opt/segment.py"]
