FROM deepinfer/prostate

# Basic env setup
COPY . /opt
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Install arterys library
RUN pip install --upgrade pip
RUN pip install git+https://github.com/fepegar/arterys#egg=arterys

EXPOSE 8000
ENTRYPOINT ["python", "/opt/segment.py"]
