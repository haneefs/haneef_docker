This project contains  3 docker images, one for standalone keystone, one for idp and one for sp
IDP and SP are still work in progress

Look into README.md for under each directory for specific instructions

# Sample instructions for mysql data base
# Here we create 3 databases one each for standalone keystone, keystone idp and keystone sp

#For Standalone kesytone with the username keystone
CREATE DATABASE keystone;
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'keystone';
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'keystone';


#For kesytone_idp with the username keystone_idp
CREATE DATABASE keystone_idp;
GRANT ALL PRIVILEGES ON keystone_idp.* TO 'keystone_idp'@'localhost' IDENTIFIED BY 'keystone_idp';
GRANT ALL PRIVILEGES ON keystone_idp.* TO 'keystone_idp'@'%' IDENTIFIED BY 'keystone_idp';

#For kesytone_sp with the username keystone_sp
CREATE DATABASE keystone_sp;
GRANT ALL PRIVILEGES ON keystone_sp.* TO 'keystone_sp'@'localhost' IDENTIFIED BY 'keystone_sp';
GRANT ALL PRIVILEGES ON keystone_sp.* TO 'keystone_sp'@'%' IDENTIFIED BY 'keystone_sp';
