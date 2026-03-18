.PHONY: all clean watch

all:
	chmod +x build.sh
	./build.sh

watch:
	chmod +x build.sh
	cd src && latexmk -lualatex -interaction=nonstopmode -pvc -synctex=1 -outdir=../dist main.tex

clean:
	rm -rf dist/*
	cd src && latexmk -c
	cd src && rm -f *.aux *.log *.out *.toc *.fls *.fdb_latexmk *.synctex.gz
