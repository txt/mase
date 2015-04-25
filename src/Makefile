out    = ../doc#
etc    = ../etc#
prefix = https://github.com/txt/mase/blob/master#


pys  = $(subst .py,.md,$(shell ls *.py;))#
mds  = $(out)/$(subst .md ,.md $(out)/,$(pys))#
Make = $(MAKE) --no-print-directory #

publish: dirs $(mds)  typo

x:
	echo $(pys)

typo:  ready
	@- git status
	@- git commit -am "saving"
	@- git push origin master

commit:  ready
	@- git status
	@- git commit -a
	@- git push origin master

update:; @- git pull origin master
status:; @- git status

ready: dirs gitting

gitting:
	@git config --global credential.helper cache
	@git config credential.helper 'cache --timeout=3600'

your:
	@git config --global user.name "Your name"
	@git config --global user.email your@email.address

timm:
	@git config --global user.name "Tim Menzies"
	@git config --global user.email tim.menzies@gmail.com

define p2md
  BEGIN	   {  
	 q="\""
	 print "" 
	 print "# " name 
	 print ""
	 First = 1      
	 In = 1
  }	 
  /^"""</,/^>"""/ {  next } 
  /^"""/	  {  In = 1 - In       
		     if (In)	    
		       print "````python"
		     else	  
		       if (First)   
			 First = 0   
		       else     
			 print "````"  
		     next }       
  ! First { print $$0 }       
  END     { if (In) print "````"  }
endef

export p2md

dirs:
	@ - mkdir -p $(out) $(etc)

$(etc)/p2md.awk  : Makefile
	 @- echo "$$p2md" > $@

$(out)/%.md: %.py $(etc)/header.txt $(etc)/footer.txt $(etc)/p2md.awk
	@echo "making... $<"
	@(cat $(etc)/header.txt; \
         awk -f $(etc)/p2md.awk -v name="$<" $< ; \
         cat $(etc)/footer.txt) \
         | sed 's?_PREFIX?$(prefix)?g' > $@;
	@git add $@
