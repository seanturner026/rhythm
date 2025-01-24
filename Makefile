.PHONY: compile-requirements
compile-requirements:
	uv pip compile requirements/base.in > requirements/requirements.txt
