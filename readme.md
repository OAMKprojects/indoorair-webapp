# Webapp part from IndoorAir-project

move indoorair-server from indoorair-raspberrypi/build-folder in this folder

run bash script : bash runserver.sh (ip-addres) (serial port)

    bash runserver.sh 192.168.x.x ttyACM0

if indoorair-raspberrypi is compiled with definition ADMIN=ON, and file indoorair-server
is in same folder, running admin server parallel with webserver can achieved with command:

    bash runserver.sh 192.168.x.x ttyACM0 admin
