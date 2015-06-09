install:
	sudo apt-get install python3
	sudo apt-get install python3-pip
	sudo pip3 install flask
	sudo pip3 install feedparser

	sudo apt-get install python-dev
	sudo apt-get install libxml2-dev libxslt-dev
	sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev

	sudo pip3 install stop-words
	sudo pip3 install newspaper3k
	sudo curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3

	sudo pip3 install PyMySQL
	sudo pip3 install Flask-SQLAlchemy
	sudo pip3 install Flask-WTF

	sudo chmod 755 dbscripts/dbsetup.sh
	sudo ./dbscripts/dbsetup.sh mti2016 mti2016

dbsetup:
	sudo ./dbscripts/dbsetup.sh mti2016 mti2016

run:
	python3 run.py
