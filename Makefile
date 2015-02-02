.PHONY: all

all: static/html/index.html static/js/game.js static/css/style.css

static/html/%.html: templates/haml/%.haml
	haml $< > $@

static/css/%.css: templates/sass/%.sass
	sass -t expanded $< > $@

static/js/%.js: templates/coffee/%.coffee
	coffee -bco $(shell dirname $@) $<
