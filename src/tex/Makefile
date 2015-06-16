Src=mase
Name=15how
BibDir=.
Bib=  $(BibDir)/refs.bib
PdfOut=../../img

.PHONY: all typo commit update status gitting timm publish one view open publocal done dirs clean tex texs one embedfonts bib

all : dirs tex bib  tex tex embedfonts done publocal

typo   : ;cd ..; $(Make) typo
commit : ;cd ..; $(Make) commit
update : ;cd ..; $(Make) update
status : ;cd ..; $(Make) status
gitting: ;cd ..; $(Make) gitting
timm   : ;cd ..; $(Make) timm

publish : dirs all
	cp $(HOME)/tmp/$(Src).pdf pdf/$(Name).pdf
	chmod a+r pdf/$(Name).pdf
	scp -p pdf/$(Name).pdf stuff@ttoy.net:menzies.us/pdf

one : dirs tex done publocal

view:
	evince $(HOME)/tmp/$(Src).pdf &

open:
	open $(HOME)/tmp/$(Src).pdf 

publocal:
	cp $(HOME)/tmp/$(Src).pdf $(PdfOut)


done :
	@printf "\n\n\n==============================================\n"
	@printf       "see output in $(HOME)/tmp/$(Src).pdf\n"
	@printf       "==============================================\n\n\n"
	@printf "\n\nWarnings (may be none):\n\n"
	@- grep arning $(HOME)/tmp/${Src}.log

dirs :
	- [ ! -d $(HOME)/tmp ] && mkdir $(HOME)/tmp
	- [ ! -d $(PdfOut) ] && mkdir $(PdfOut)

SRC=$(wildcard *.md)
TEX=$(SRC:.md=.tex)


%.md : ../%.py
	./p2md $< > $@	

clean:
	rm $(HOME)/tmp/$(Src)*

texs: lib.md $(TEX) 
tex : texs tmptex bib tmptex

tmptex :
	@pdflatex --shell-escape -output-directory=$(HOME)/tmp $(Src).tex		

%.tex:	%.md
	pandoc -r markdown+simple_tables+table_captions+yaml_metadata_block \
	       -w latex \
                --filter pandoc-citeproc \
               --csl=ieee.csl --bibliography=$(Bib) \
               -o - $< | sed 's/{verbatim}/{lstlisting}/' > $@

embedfonts:
	@ gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite \
          -sOutputFile=$(HOME)/tmp/$(Src)-embedded.pdf $(HOME)/tmp/$(Src).pdf
	@ mv              $(HOME)/tmp/$(Src)-embedded.pdf $(HOME)/tmp/$(Src).pdf

bib :
	- cp $(Bib) $(HOME)/tmp; cd $(HOME)/tmp; bibtex $(Src)
