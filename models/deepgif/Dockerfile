FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

# Basic env setup
COPY . /opt
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
RUN apt-get update

# Install Conda
RUN apt-get install -y git curl
RUN curl --location --remote-name http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda
RUN conda install python=3.6 -y

# Install libraries
RUN conda install pytorch==1.2.0 cudatoolkit=10.0 -c pytorch -y
RUN pip install git+https://github.com/fepegar/arterys#egg=arterys
RUN pip install highresnet==0.10.0

# Print some GPU info
RUN python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
RUN nvcc --version

EXPOSE 8000
ENTRYPOINT ["/miniconda/bin/python", "/opt/segment.py"]
