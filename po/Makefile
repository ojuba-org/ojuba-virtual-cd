POTFILE=$(shell cat POTFILES.in)
SOURCES=$(addprefix ../, $(POTFILE))
POFILES=$(wildcard *.po)
MOFILES=$(patsubst %.po,%.mo,$(POFILES))

all: ojuba-virtual-cd.pot $(MOFILES)

ojuba-virtual-cd.pot: $(SOURCES)
	echo $(SOURCES)
	intltool-update -g ojuba-virtual-cd -p

%.mo: %.po
	msgfmt $*.po -o $*.mo
	mkdir -p ../locale/$*/LC_MESSAGES/ || :
	cp $*.mo ../locale/$*/LC_MESSAGES/ojuba-virtual-cd.mo

%.po: ojuba-virtual-cd.pot
	intltool-update -g ojuba-virtual-cd -d $*

