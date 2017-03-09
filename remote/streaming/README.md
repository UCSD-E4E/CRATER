`deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ jessie main`
`sudo apt-get update`
`sudo apt-get install uv4l uv4l-raspicam`
`sudo apt-get install uv4l-raspicam-extras`
Enable rpicam via raspi-config
`sudo apt-get install uv4l-server uv4l-uvc uv4l-xscreen uv4l-mjpegstream uv4l-dummy uv4l-raspidisp`
`sudo apt-get install uv4l-webrtc`
`openssl genrsa -out selfsign.key 2048 && openssl req -new -x509 -key selfsign.key -out selfsign.crt -sha256`
Goto `https://raspberry:8080`