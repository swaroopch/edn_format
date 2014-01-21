all: test install

test:
	python tests.py

install:
	python setup.py clean
	python setup.py install
