.PHONY: test1 test2 test3 test4

test1:
	python routenode.py dv r 123 1111 2222 1 3333 50

test2:
	python routenode.py dv r 123 1111 2222 1 3333 2

test3:
	python routenode.py dv r 123 3333 1111 50 2222 2 last 60