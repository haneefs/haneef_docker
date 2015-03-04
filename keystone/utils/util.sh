keystone --os-token ADMIN user-create --name admin --pass admin
keystone --os-token ADMIN role-create --name admin
keystone --os-token ADMIN tenant-create --name admin
keystone --os-token ADMIN user-role-add --user admin --tenant admin --role admin
