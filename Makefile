.PHONY: test1 test2 test3 test4

test1:
	python routenode.py dv r 123 1111 2222 1 3333 50

test2:
	python routenode.py dv r 123 2222 1111 1 3333 2 4444 8

test3:
	python routenode.py dv r 123 3333 1111 50 2222 2 4444 5

test4:
	python routenode.py dv r 123 4444 2222 8 3333 5 last 2