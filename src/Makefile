root   = ..#
out    = .#
etc    = ../etc#
prefix = https://github.com/txt/mase/blob/master#
img=https://raw.githubusercontent.com/txt/mase/master/img#

pys  = $(subst .py,.md,$(shell ls *.py;))#
mds  = $(out)/$(subst .md ,.md $(out)/,$(pys))#
Make = $(MAKE) --no-print-directory #

publish: parts typo

parts: dirs zaps $(mds) $(root)/toc.md 

typo   : ;cd ..; $(Make) typo
commit : ;cd ..; $(Make) commit
update : ;cd ..; $(Make) update
status : ;cd ..; $(Make) status
gitting: ;cd ..; $(Make) gitting
timm   : ;cd ..; $(Make) timm

ready: dirs gitting chmods

zaps:
	find . -name '*.pyc' | xargs -n 25 rm 

chmods:
	chmod +x *ok.py

define p2md
  BEGIN	   {  
	 q="\""
	 First = 1      
	 In = 1
  }
  /^"""</,/^>"""/ {  next } 
  /^"""/	  {  Once = 1
                     In = 1 - In       
		     if (In) 
		       print "````python"
		     else	  
		       if (First)   
			 First = 0   
		       else     
			 print "````"  
		     next }       
  ! First {  pre = In ? sprintf("% 4s:   ",++line) : ""
             print pre $$0 }       
  END     { if (In ) print "````"
            if (!Once) print "```"  
}
endef
export p2md

define toc
echo ""
echo "# Table of Contents"
echo ""
files=`ls [0-9a-z]*.py | grep -v "ok.py"`
for f in $$files; do
   awk ' gsub(/^# /,"") {
         name=$$0
	 file=FILENAME
         gsub(/.py$$/,".md",file)
         print "+ ["$$0"](__PRE/doc/"file")"; 
         exit}' $$f
done
echo ""   
endef
export toc

tocs : $(root)/TOC.md


dirs:
	@ - mkdir -p $(out) $(etc)

$(etc)/p2md.awk : Makefile ; @- echo "$$p2md" > $@
$(etc)/toc.sh   : Makefile ; @- echo "$$toc"  > $@

$(out)/%.md: %.py $(etc)/header.txt $(etc)/footer.txt $(etc)/p2md.awk
	@echo "making... $<"
	@(cat $(etc)/header.txt; \
          echo "<small><em>View <a href=\"$<\">source</a></em></small>"; \
         awk -f $(etc)/p2md.awk -v name="$<" $< ; \
         cat $(etc)/footer.txt) \
         | sed 's?__PRE?$(prefix)?g'  \
         | sed 's?__IMG?$(img)?g' > $@;
	@git add $@

$(root)/toc.md:  Makefile $(etc)/header.txt $(etc)/footer.txt $(etc)/p2md.awk
	@echo "making... $(root)/TOC.md"
	@(cat $(etc)/header.txt; \
          bash $(etc)/toc.sh   ; \
          cat $(etc)/footer.txt) \
          | sed 's?__PRE?$(prefix)?g'  \
          | sed 's?__IMG?$(img)?g' > $(root)/TOC.md 
	@git add $@


