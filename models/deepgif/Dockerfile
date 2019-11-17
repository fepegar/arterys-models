FROM nvidia/cuda:9.0-cudnn7-devel

# Basic env setup
COPY . /opt
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Install arterys library
RUN apt-get update && apt-get install -y python3 python3-pip git
RUN pip install --upgrade pip
RUN pip install git+https://github.com/fepegar/arterys#egg=arterys
RUN pip install torch
RUN pip install highresnet

EXPOSE 8000
ENTRYPOINT ["python3", "/opt/segment.py"]
