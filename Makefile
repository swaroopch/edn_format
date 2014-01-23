all: test install

clean:
	rm -rf build/
	python setup.py clean

test: clean
	python tests.py

install: clean
	python setup.py install
