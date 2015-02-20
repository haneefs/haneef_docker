To build
docker build --tag haneef/keystone_standalone .


You need to mount 2 directories. One has configuration and other has logs

Contents of /etc/keystone directory
1. keystone.conf
	This you can copy from samples/conf directory. Edit the sql connection string to point to your database
2. logging.conf
	This you can copy from samples/conf directory.
3. policy.conf
	You can get this files from  keystone repo  under /etc directory
	https://github.com/openstack/keystone/blob/master/etc/policy.json
4. keystone-paste.ini
	You can get this files from  keystone repo  under /etc directory
	https://github.com/openstack/keystone/blob/master/etc/keystone-paste.ini


Running keystone standalone container

For interactive mode
docker run -ti -v /etc/keystone:/etc/keystone  -v /var/log/keystone:/var/log/keystone -p 35357:35357  --name keystone_standalone haneef/keystone_standalone  /bin/bash

#Now you will be inside the container. Run the next command inside the container
service apache2 restart 

#Verification
curl -k http://localhost:35357   #If this throws error, then look at /var/log/keystone/keystone_modwsgi.log. Most probably you won't have permission for /var/log/keystone directory



If everything works, from next time onwards you can run in non-interactive mode
#Create a directory /var/log/keystone in the host for log contents
To run 
docker run -d -v /etc/keystone:/etc/keystone -v /var/log/keystone:/var/log/keystone -p 35357:35357  --name keystone_standalone haneef/keystone_standalone 


