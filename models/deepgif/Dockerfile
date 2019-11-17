FROM nvidia/cuda:9.0-cudnn7-devel

# Basic env setup
COPY . /opt
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Install arterys library
RUN apt-get update && apt-get install -y python3 python3-pip git
RUN pip3 install --upgrade pip
RUN pip3 install git+https://github.com/fepegar/arterys#egg=arterys
RUN pip3 install torch==1.3.0
RUN pip3 install highresnet==0.10.0

EXPOSE 8000
ENTRYPOINT ["python3", "/opt/segment.py"]
