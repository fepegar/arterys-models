FROM deepinfer/prostate
# RUN apt-get update && apt-get install -y python3 python3-pip git

# Basic env setup
COPY . /opt
RUN ls -lah /opt
# RUN python --version
# RUN python3 --version
# RUN which pip
# RUN which pip3
# RUN pip install --upgrade pip
RUN pip install git+https://github.com/fepegar/arterys#egg=arterys
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

EXPOSE 8000
ENTRYPOINT ["python", "/opt/segment.py"]
