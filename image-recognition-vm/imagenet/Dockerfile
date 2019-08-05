FROM tensorflow/tensorflow
MAINTAINER TanLong "tanlong.siau@dell.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
#RUN mkdir -p /opt/models/tutorials/image/imagenet

WORKDIR /opt/models/tutorials/image/imagenet
ADD requirements.txt /opt/models/tutorials/image/imagenet/
RUN pip install -r requirements.txt
ADD *.* /opt/models/tutorials/image/imagenet/
#RUN apt-get install -y protobuf-compiler python-pil python-lxml

#WORKDIR /opt/models/research/object_detection/protos
#ADD *.* /opt/models/research/object_detection/protos/
#WORKDIR /opt/models/research
#RUN export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

#RUN mkdir -p /tmp/imagenet/
#ADD /opt/models/tutorials/image/imagenet/inception-2015-12-05.tgz /tmp/imagenet/

EXPOSE 5000

WORKDIR /opt/models/tutorials/image/imagenet
CMD [ "python", "./tensorflow-server.py" ]
