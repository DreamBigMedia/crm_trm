#!/bin/bash
DOMAIN=$1
CRM_HOST=162.218.236.81
echo 'deb http://packages.dotdeb.org wheezy all' >> /etc/apt/sources.list
echo 'deb-src http://packages.dotdeb.org wheezy all' >> /etc/apt/sources.list
apt-get -y update
apt-get -y upgrade
apt-get -y install nginx sed
sed "s/DOMAIN/${DOMAIN}/g" nginx-remote.conf | sed "s/CRM_HOST/${CRM_HOST}/g" -- > /etc/nginx/sites-available/$DOMAIN
mkdir -p /var/www/$DOMAIN/htdocs
mkdir -p /var/www/$DOMAIN/certs
cd /var/www/$DOMAIN/certs
openssl req -out $DOMAIN.csr -new -newkey rsa:2048 -nodes -keyout server.key
cp $DOMAIN.csr ../htdocs/somethingrandom
cd ../htdocs
cat somethingrandom
echo "Certificate Signing Request also available at http://${DOMAIN}/somethingrandom"
