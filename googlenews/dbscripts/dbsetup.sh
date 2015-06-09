#!/bin/bash

EXPECTED_ARGS=2
E_BADARGS=65
MYSQL=`which mysql`

Q2="GRANT USAGE ON *.* TO $1@localhost IDENTIFIED BY '$2';"
Q3="GRANT ALL PRIVILEGES ON googlenewsdb.* TO $1@localhost;"
Q4="FLUSH PRIVILEGES;"
SQL="${Q2}${Q3}${Q4}"

echo "Database setup processing..."

if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0 dbuser dbpass"
  exit $E_BADARGS
fi

echo "Database creation processing..."
sudo $MYSQL -uroot -p <  dbscripts/googlenewsdb.sql

echo "User creation processing..."
sudo $MYSQL -uroot -p -e "$SQL"

# Let the user know something good just happened

echo "Database creation of googlenewsdb complete."
echo "Access with username $1 and password $2. Pass!"