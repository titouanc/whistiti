# Whistiti

A pretext project to use the hypest web technologies:

* crossbar.io and Autobahn
* HAML, SASS, Coffeescript

## Requirements

Requirements for the python project coul be installed with

	virtualenv ve
	source ve/bin/activate
	pip install -r requirements.txt

To compile the templates, you need the 3 programs `haml`, `sass` and `coffee`, and also `make`.
The compiled versions of the templates are in the repo if you just want to test the frontend without hacking it.

## Run it !

```shell
crossbar start # Start the wamp broker
make           # Compile templates
pythapp.py     # Start the main app
```
