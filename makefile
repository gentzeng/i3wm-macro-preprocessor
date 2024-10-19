# Detect Python 3 executable
PYTHON := $(shell which python3 || which python || echo "Python not found")
ifeq ($(PYTHON), "Python not found")
$(error Python 3 not found. Please install Python 3.)
endif

install: compile
	mkdir -p ~/.i3
	cp ./config ~/.i3/

compile:
	cp ./configSource ./config
	$(PYTHON) ./configMarkoCompiler/configMarkoCompiler.py ./config

clean:
		rm -rf __pycache__

test:
	$(PYTHON) configMarkoCompiler/test.py

.PHONY: install compile clean test
