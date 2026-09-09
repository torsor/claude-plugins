.PHONY: check test audit enable-hooks

check: test audit

test:
	python3 -m unittest discover -s tests -v

audit:
	bash plugins/torsor-writing/scripts/audit-public.sh --history

enable-hooks:
	git config core.hooksPath .githooks
