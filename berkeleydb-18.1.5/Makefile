.PHONY: build docs dist

full-test:
	./test-full_prerelease.py

dist: clean docs
	YES_I_HAVE_THE_RIGHT_TO_USE_THIS_BERKELEY_DB_VERSION=1 \
		DISTUTILS_DEBUG=1 \
		./setup.py sdist

clean: docs-clean
	rm -rf build dist __pycache__ tests/__pycache__

docs-clean:
	cd docs && $(MAKE) clean

docs:
	cd docs && $(MAKE) html
