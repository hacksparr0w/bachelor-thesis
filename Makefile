.DEFAULT_GOAL := build

build:
	mkdir -p ./.miktex

	docker run \
	-it \
	-v $(shell pwd)/.miktex/:/miktex/.miktex \
	-v $(shell pwd):/miktex/work \
	$(shell docker build -q .) \
	`pdflatex --shell-escape -output-directory=./ main.tex && biber main.bcf && pdflatex --shell-escape -output-directory=./ main.tex`
