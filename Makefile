.DEFAULT_GOAL := build

build:
	docker run \
	-v $(shell pwd):/build \
	$(shell docker build -q .) \
	make tex

tex:
	pdflatex --shell-escape -output-directory=./ main.tex
	biber main.bcf
	pdflatex --shell-escape -output-directory=./ main.tex
