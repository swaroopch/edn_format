test:
	python tests.py

all: test
	python setup.py clean
	python setup.py install
