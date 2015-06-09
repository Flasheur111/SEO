# SEO

Chaîne de traitement pour Google News
====================================

Installation :
------------
1) Install mysql and start the service.

2) Install python 3.x.x.

3) Install the dependencies & create the database & run the server with:

	* make

4) You should then see the following:

	* Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)

	* Restarting with stat

5) Go to http://127.0.0.1:8080/ to start using the app!

If you want to go through each step of the setup manually:

1) Install the dependencies with:

	* make install

2) Create the database and its user with:

	* make dbsetup

3) Start the application server with:

	* make run
