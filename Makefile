PY = pyhton
PFLAGS =

ARG = 100

make_data:
	python3 make_data.py ${ARG}

burnes_hut:
	python3 burnes_hut.py
