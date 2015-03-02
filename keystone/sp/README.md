To build
docker build --tag haneef/keystone_sp .

Running keystone sp container

For interactive mode
docker run -ti -v /etc/keystone_sp:/etc/keystone  -v /var/log/keystone_sp:/var/log/keystone -p 35358:35358  --name keystone_sp haneef/keystone_sp  /bin/bash





