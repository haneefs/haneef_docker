To build
docker build --tag haneef/keystone_idp .

Running keystone idp container

For interactive mode
docker run -ti -v /etc/keystone_idp:/etc/keystone  -v /var/log/keystone_idp:/var/log/keystone -p 35357:35357  --name keystone_idp haneef/keystone_idp  /bin/bash





