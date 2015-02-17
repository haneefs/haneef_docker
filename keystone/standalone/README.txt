To build
docker build --tag haneef/keystone_standalone .

#Create a directory /var/log/keystone in the host for log contents
To run 
docker run -d -v /etc/keystone:/etc/keystone -v /var/log/keystone:/var/log/keystone -p 35357:35357  --name keystone_standalone haneef/keystone_standalone 

For interactive mode
docker run -ti -v /etc/keystone:/etc/keystone  -v /var/log/keystone:/var/log/keystone -p 35357:35357  --name keystone_standalone haneef/keystone_standalone  /bin/bash
service apache2 restart # Run this in the container
