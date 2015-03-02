############################################################
# Based on Ubuntu Image
# Dockerfile to run keystone
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu:trusty

# Set the file maintainer (your name - the file's author)
MAINTAINER Haneef Ali
ENV REFRESHED_AT 2014-11-0

# Use this environment variable to get any release
ENV GIT_TAG  master

# Update the default application repository sources list
RUN apt-get update

# Install  utilities
RUN apt-get install -y curl git 

# Install development packages to build 
RUN apt-get install -y curl git python-dev python-pip python-mysqldb xmlsec1
RUN apt-get install -y libsqlite3-dev libldap2-dev libsasl2-dev libssl-dev libxml2-dev libxslt1-dev libffi-dev

#Install Apache2 and configure mod wsgi
RUN apt-get install -y apache2
RUN apt-get install -y libapache2-mod-wsgi libssl-dev libffi-dev 

# Make dir and clone openstack
RUN mkdir -p /opt/stack/openstack/

RUN cd /opt/stack/openstack &&  git clone https://github.com/openstack/keystone

WORKDIR /opt/stack/openstack/keystone
RUN  git checkout $GIT_TAG -tb origin/$GIT_TAG
RUN  pip install -U -r ./requirements.txt 

#Install the test dependencies as LDAP and saml are part of it
RUN  pip install -U -r ./test-requirements.txt  
RUN  python setup.py install

#Required if you  use LDAP backend
RUN pip install -U python-ldap 

#Install Apache2 mod-shlib2 - Required for federation
RUN apt-get install -y  libapache2-mod-shib2

ADD keystone-modwsgi.conf  /etc/apache2/sites-available/
RUN a2ensite keystone-modwsgi

ENV KEYSTONE_USER keystone
RUN useradd -MU keystone

#Latest version of modwsgi doesn't work without home directory
#Just create a empty directory

RUN mkdir -p /home/keystone

RUN mkdir -p /var/www/keystone/ 
RUN ln -s /opt/stack/openstack/keystone/httpd/keystone.py /var/www/keystone/admin
RUN ln -s /opt/stack/openstack/keystone/httpd/keystone.py /var/www/keystone/main

#Volume for configuration files
VOLUME ["/var/log/keystone" , "/etc/keystone"]

#Change the owners of log file to keystone
RUN chown -R keystone /var/log/keystone

#Add sample configuration files for reference
ADD  sample/conf /etc/keystone_conf_sample

# Port to expose 
EXPOSE 35357

#Install openstackclient as only openstackclient supports v3 operations
RUN cd /opt/stack/openstack &&  git clone https://github.com/openstack/python-openstackclient.git
WORKDIR /opt/stack/openstack/python-openstackclient
RUN  git checkout $GIT_TAG -tb origin/$GIT_TAG
RUN  python setup.py install

# By default, simply start apache.
#CMD /usr/sbin/apache2ctl -D FOREGROUND

