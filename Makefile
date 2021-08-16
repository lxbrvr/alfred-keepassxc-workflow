help:
	@echo "Command          Description"
	@echo ""
	@echo "test             runs tests"
	@echo "vtest            runs tests with increased verbosity"
	@echo "cov-run          runs coverage"
	@echo "cov-report       shows coverage report without 100% covered files"
	@echo "cov-html         generates html coverage report without 100% covered files"
	@echo "latest-version   shows the latest version of the project"
	@echo "beautify         formats the code using different rules"
	@echo "install          installs the workflow for development"
	@echo "prepare_plist    removes all env variables not allowed for export and updates with meta information"
	@echo "build            prepares info.plist and creates a workflow file (keepassxc.alfredworkflow) from the source code"

test:
	@PYTHONPATH=$(PWD)/src pytest -s $(path)

vtest:
	@PYTHONPATH=$(PWD)/src pytest -s -vv $(path)

cov-run:
	@PYTHONPATH=$(PWD)/src coverage run --source=src -m pytest -q

cov-report: cov-run
	@coverage report --skip-covered

cov-html: cov-run
	@coverage html --skip-covered

latest-version:
	@git fetch && git describe --tags --abbrev=0

beautify:
	@isort \
		-m 3 \
		--apply \
		--recursive \
		--lines=79 \
		--trailing-comma \
		src tests

install:
	@python scripts/install.py --source=$(PWD)/src

prepare_plist:
	@python scripts/prepare_plist.py \
		--source=$(PWD)/src \
		--version=$(version) \
		--bundle_id=com.lxbrvr.keepassxcalfred

build: test
	@python scripts/build.py --source=$(PWD)/src --version=$(version)
