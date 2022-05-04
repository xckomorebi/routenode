.PHONY: clean_cache dvr1 dvr2 dvr3 dvr4 dvp1 dvp2 dvp3 ls1 ls2 ls3 ls4

clean_cache:
	find . -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Only for testing

# distance vector, regular
dvr1:
	PA2_DEBUG=1 python routenode.py dv r 123 1111 2222 1 3333 50

dvr2:
	PA2_DEBUG=1 python routenode.py dv r 123 2222 1111 1 3333 2 4444 8

dvr3:
	PA2_DEBUG=1 python routenode.py dv r 123 3333 1111 50 2222 2 4444 5

dvr4:
	PA2_DEBUG=1 python routenode.py dv p 123 4444 2222 8 3333 5 last 2

#distance vector, poison
dvp1:
	PA2_DEBUG=1 python routenode.py dv p 123 1111 2222 1 3333 50

dvp2:
	PA2_DEBUG=1 python routenode.py dv p 123 2222 1111 1 3333 2

dvp3:
	PA2_DEBUG=1 python routenode.py dv p 123 3333 1111 50 2222 2 last 60

# link state
ls1: 
	PA2_DEBUG=1 python routenode.py ls r 5 1111 2222 1 3333 50
ls2: 
	PA2_DEBUG=1 python routenode.py ls r 5 2222 1111 1 3333 2 4444 8
ls3: 
	PA2_DEBUG=1 python routenode.py ls r 5 3333 1111 50 2222 2 4444 5
ls4: 
	PA2_DEBUG=1 python routenode.py ls r 5 4444 2222 8 3333 5 last 20
