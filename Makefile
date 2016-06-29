.PHONY: build clean release

build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist

release: clean build
	twine upload -s  -i tonyseek@gmail.com dist/*
