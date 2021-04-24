#!/bin/bash
if [ $# -lt 2 ]; then 
	echo "Enter ip-addres and serial port"
	exit 1
fi
echo "Starting nucleo server..."
if [ -z "$3" ]; then
	./indoorair-server "$2" > /dev/null 2>&1 &
else
	sudo ./indoorair-server "$2" "$3" &
fi
echo "Starting webserver..."
echo
python3 indoorair.py "$1"
echo
echo "Terminating nucleo server..."
kill -9  $(ps aux | grep '[i]ndoorair' | awk '{print $2}')

