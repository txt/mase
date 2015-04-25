root=../..#
etc=$(root)/etc#
prefix = https://github.com/txt/mase/blob/master#
img=https://raw.githubusercontent.com/txt/mase/master/img#

mds=$(shell ls *.md)
outs=$(root)/$(subst .md ,.md $(root)/,$(mds))
Make = $(MAKE) --no-print-directory #

all: publish typo

publish: $(outs) 

$(root)/%.md : %.md $(etc)/header.txt $(etc)/footer.txt $(etc)/p2md.awk
	@echo "making... $@"
	@(cat $(etc)/header.txt  $<  $(etc)/footer.txt) \
	| sed 's?__PRE?$(prefix)?g' \
        | sed 's?__IMG?$(img)?g' > $@;
	@git add $@

typo   : ;cd ..; $(Make) typo
commit : ;cd ..; $(Make) commit
update : ;cd ..; $(Make) update
status : ;cd ..; $(Make) status
gitting: ;cd ..; $(Make) gitting
timm   : ;cd ..; $(Make) timm
