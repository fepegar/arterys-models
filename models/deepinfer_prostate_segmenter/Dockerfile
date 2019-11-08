FROM deepinfer/prostate

# Basic env setup
COPY . /opt
RUN ls -lah /opt
RUN pip install git+https://github.com/fepegar/arterys#egg=arterys
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

EXPOSE 8000
ENTRYPOINT ["python", "/opt/segment.py"]
