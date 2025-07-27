# A GNU Makefile to run various tasks - compatibility for us old-timers.

# Note: This makefile include remake-style target comments.
# These comments before the targets start with #:
# remake --tasks to shows the targets and the comments

GIT2CL ?= admin-tools/git2cl
PYTHON ?= python3
PIP ?= pip3
BASH ?= bash
RM  ?= rm

.PHONY: \
	all \
	check \
	clean \
	dist \
	rmChangeLog \
	ChangeLog

#: Default target - same as "develop"
all: develop

develop:
	$(PIP) install -e .[dev]

#: Clean up temporary files
clean:
	find . | grep -E '\.pyc' | xargs rm -rvf;
	find . | grep -E '\.pyo' | xargs rm -rvf;
	$(PYTHON) ./setup.py $@

#: Make distribution: wheel and tarball
dist:
	./admin-tools/make-dist.sh

#: Install trepan3k-mathics3
install:
	$(PIP) install -e .

#: Remove ChangeLog
rmChangeLog:
	$(RM) ChangeLog || true

#: Create a ChangeLog from git via git log and git2cl
ChangeLog: rmChangeLog
	git log --pretty --numstat --summary | $(GIT2CL) >$@

.PHONY: $(PHONY)
