SHELL=/bin/bash

TOPdir=${HOME}


###############################################

CHMOD = chmod +x
CP    = cp -a
MKDIR = mkdir -p
SED   = sed -i

PROJNAME=emulation
BUILDdir=build
RELEASEdir=release
TESTDIR = $(BUILDdir)/test


all: create_build_env replace_topdir $(PROJNAME)_types $(PROJNAME) release

clean depend generated realclean check-syntax $(CUSTOM_TARGETS):
	rm -rf build
	rm -rf $(RELEASEdir)

.PHONY: $(PROJNAME)_types
$(PROJNAME)_types:
	mkdir -p $(BUILDdir)
	cd $(BUILDdir) && $(MAKE) -f ../Makefile.$(PROJNAME)_types all

.PHONY: $(PROJNAME)
$(PROJNAME): $(PROJNAME)_types
	cd $(BUILDdir) && $(MAKE) -f ../Makefile.$(PROJNAME) all

create_build_env:
	$(MKDIR) $(BUILDdir)
	$(CP) src/* $(BUILDdir)/
	$(CP) agentworker $(BUILDdir)/
	$(CP) Makefile.install $(BUILDdir)/

replace_topdir:
	$(SED) 's/{TOPdir}/$(subst /,\/,${TOPdir})/g' $(BUILDdir)/agentworker/agent-wrap.sh
	$(SED) 's/{TOPdir}/$(subst /,\/,${TOPdir})/g' $(BUILDdir)/agentworker/testbed-agent.service
	$(SED) 's/{TOPdir}/$(subst /,\/,${TOPdir})/g' $(BUILDdir)/agentworker/config.py
	$(SED) 's/{TOPdir}/$(subst /,\/,${TOPdir})/g' $(BUILDdir)/Manager.hpp
	$(SED) 's/{TOPdir}/$(subst /,\/,${TOPdir})/g' $(BUILDdir)/Makefile.install

release:
	$(MKDIR) $(RELEASEdir)/lib
	$(CP) INSTALL.md $(RELEASEdir)/
	$(CP) $(BUILDdir)/agentworker $(RELEASEdir)/
	$(CP) $(BUILDdir)/Makefile.install $(RELEASEdir)/Makefile
	$(CP) $(BUILDdir)/$(PROJNAME) $(RELEASEdir)/emulation
	$(CP) $(BUILDdir)/*.so $(RELEASEdir)/lib
	$(CHMOD) $(RELEASEdir)/agentworker/agent-wrap.sh
	$(CHMOD) $(RELEASEdir)/emulation

.PHONY: test
test: $(PROJNAME)_types
	${MKDIR} $(TESTDIR)
	cd $(TESTDIR) && $(MAKE) -C ../../test test

test_dds: $(PROJNAME)_types
	${MKDIR} $(TESTDIR)
	cd $(TESTDIR) && $(MAKE) -C ../../test test_dds

test_loss_rate: $(PROJNAME)_types
	${MKDIR} $(TESTDIR)
	cd $(TESTDIR) && $(MAKE) -C ../../test test_loss_rate

test_measure: $(PROJNAME)_types
	${MKDIR} $(TESTDIR)
	cd $(TESTDIR) && $(MAKE) -C ../../test test_measure

test_saver: $(PROJNAME)_types
	${MKDIR} $(TESTDIR)
	cd $(TESTDIR) && $(MAKE) -C ../../test test_saver
