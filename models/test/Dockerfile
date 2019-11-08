FROM nvidia/cuda:9.0-cudnn7-devel
RUN apt-get update && apt-get install -y python3 python3-pip git

# Basic env setup
WORKDIR /opt
COPY . /opt
RUN pip3 install --upgrade pip
RUN pip3 install git+https://github.com/fepegar/arterys-test#egg=arterys
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

EXPOSE 8000
ENTRYPOINT ["segment"]
