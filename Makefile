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

ready: gitting zaps
zaps:
	find . -name '*.pyc' | xargs -n 50 rm

gitting:
	@git config --global credential.helper cache
	@git config credential.helper 'cache --timeout=3600'

timm:
	@git config --global user.name "Tim Menzies"
	@git config --global user.email tim.menzies@gmail.com

