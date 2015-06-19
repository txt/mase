# File:  setup/Makefile (from github.com/txt/evil)
# Usage: make
typo:   ready
	@- git status
	@- git commit -am "saving"
	@- git push origin master # update as needed

commit: ready
	@- git status
	@- git commit -a
	@- git push origin master

update: ready
	@- git pull origin master

status: ready
	@- git status

ready:
	@git config --global credential.helper cache
	@git config credential.helper 'cache --timeout=3600'

timm:  # <== change to your name
	@git config --global user.name "Tim Menzies" #<== your name
	@git config --global user.email tim.menzies@gmail.com #<== your email

tests: *ok.py
	@$(foreach f,$^,\
             printf "\n========= $f =========\n\n";\
             python $f;)
