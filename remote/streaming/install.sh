#!/bin/bash
# Enable rpicam via raspi-config
cat "deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ jessie main" >> /etc/apt/sources.list
sudo apt-get update
sudo apt-get install uv4l uv4l-raspicam uv4l-raspicam-extras uv4l-server uv4l-uvc uv4l-xscreen uv4l-mjpegstream uv4l-dummy uv4l-raspidisp uv4l-webrtc
openssl genrsa -out selfsign.key 2048
openssl req -new -x509 -key selfsign.key -out selfsign.crt -sha256
# Goto `https://raspberry:8080`