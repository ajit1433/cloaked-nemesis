#!/bin/bash

echo $(date) > log.txt
echo $(hostname) >> log.txt
echo $(ifconfig | grep addr) >> log.txt
echo $(ifconfig | grep 'inet addr' | grep Bcast | awk '{ print $2 }') >> log.txt

if [ "$(id -u)" != "0" ]
then 
	echo "This script needs to be run as root"  >> log.txt
	exit 1
fi


apt-get -y update --fix-missing >> log.txt #some trouble in digital ocean
apt-get install -y python-pip   >> log.txt #must for python
pip install requests >> log.txt

# Redirect stderr to stdout and then stdout to /dev/null
t=$(python -V 2>&1 > /dev/null | grep Python -c)

if [ $t -gt 0 ] 
then 
	echo "Python is installed" >> log.txt
else
	echo "python not installed. Updating System please w8..." >> log.txt
	#apt-get -y update >> log.txt
	apt-get -y install build-essential >> log.txt
	apt-get -y install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev >> log.txt
	apt-get -y install python python-dev >>log.txt
fi
echo "SUCCESS" >> log.txt
exit 0
