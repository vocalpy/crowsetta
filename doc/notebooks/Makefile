DATA_FORMAT_DIRS=$(wildcard ./data/*/)
IPYNB_HERE=$(wildcard ./*.ipynb)
IPYNB_WITHOUT_RAW=$(patsubst ./%.ipynb, ../../notebooks/%.ipynb, $(IPYNB_HERE))
RST_FROM_IPYNB=$(patsubst ./%.ipynb, ../%.rst, $(IPYNB_HERE))
PY_HERE=$(wildcard ./*.py)
PY_FILES=$(patsubst ./%.py, ../../notebooks/%.py, $(PY_HERE))
MAT_HERE=$(wildcard ./*.mat)
MAT_FILES=$(patsubst ./%.mat, ../../notebooks/%.mat, $(MAT_HERE))

## all			: make all targets
.PHONY: all
all : ipynb_without_raw rst_from_ipynb copy_py_and_mat

## copy_py_and_mat	: copy .py and .mat files from ./doc/notebooks to crowsetta/notebooks
copy_py_and_mat : $(PY_FILES) $(MAT_FILES)

../../notebooks/%.mat : ./%.mat
	cp -f $< $@

../../notebooks/%.py : ./%.py
	cp -f $< $@

## ipynb_without_raw	: copy notebooks into crowsetta/notebooks, but remove raw cells (with rst directives)
ipynb_without_raw : $(IPYNB_WITHOUT_RAW)

../../notebooks/%.ipynb : ./%.ipynb
	jupyter nbconvert --to notebook $< --output=$@ --TemplateExporter.exclude_raw=True

## rst_from_ipynb	: convert notebooks into rst; raw cells containing rst directives will be kept
rst_from_ipynb : $(RST_FROM_IPYNB)

../%.rst : ./%.ipynb
	jupyter nbconvert --to rst $< --output=$@

## variables		: show variables defined in this makefile
.PHONY: variables
variables :
	@echo	       ALL_FILES: 	$(ALL_FILES)
	@echo   DATA_FORMAT_DIRS:	$(DATA_FORMAT_DIRS)
	@echo         IPYNB_HERE:	$(IPYNB_HERE)
	@echo  IPYNB_WITHOUT_RAW:	$(IPYNB_WITHOUT_RAW)
	@echo     RST_FROM_IPYNB:	$(RST_FROM_IPYNB)
	@echo            PY_HERE:	$(PY_HERE)
	@echo           PY_FILES:	$(PY_FILES)	
	@echo           MAT_HERE:	$(MAT_HERE)
	@echo          MAT_FILES:	$(MAT_FILES)

## clean		: remove auto-generated files
.PHONY: clean
clean :
	rm -rf $(DATA_FORMAT_DIRS)
	rm -rf $(IPYNB_WITHOUT_RAW)
	rm -rf $(RST_FROM_IPYNB)
	rm -rf $(PY_FILES)
	rm -rf $(MAT_FILES)

.PHONY : help
## help		: Display help for this Makefile.
help : Makefile
	@sed -n 's/^##//p' $<

