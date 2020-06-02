CXX           = g++
LD            = $(CXX) $(CFLAGS)
RM            = rm -rf
CP            = cp -a
MKDIR         = mkdir -p

CFLAGS        = -Wall -std=c++11 -fPIC -O3 -g -DDEBUG $(INCLUDES)
LDFLAGS       = -L$(PWD)/../ -L. -L$(OSPL_HOME)/lib
INCLUDES      = -I$(PWD)/../ -I. -I../src -I$(OSPL_HOME)/include/dcps/C++/SACPP
LDLIBS        = -lgtest_main -lgtest -lpthread -ljsoncpp -lemulation_types -ldcpssacpp -lddskernel -ldl
LD_LIB_PATH   = "$(LD_LIBRARY_PATH):$(PWD)/../"
OUTPUT        = -o "$@"

COMPILE.cc    = $(CXX) $(CFLAGS) -c
LINK.cc       = $(LD) $(LDFLAGS)

TESTDATADIR   = ./data
OBJDIR        = $(PWD)/.obj
REPORTDIR        = $(PWD)/report

OBJS_DDS      = $(OBJDIR)/loader.o \
				$(OBJDIR)/ddsentitymanager.o \
				$(OBJDIR)/measure_receiver.o \
				$(OBJDIR)/measure_sender.o \
				$(OBJDIR)/receiver.o \
				$(OBJDIR)/sender.o \
				$(OBJDIR)/runner.o

OBJS          = $(OBJDIR)/test_monitor.o \
				$(OBJDIR)/test_loader.o \
				$(OBJDIR)/test_dds.o \
				$(OBJDIR)/test_loss_rate.o \
				$(OBJDIR)/test_measure.o \
				$(OBJDIR)/test_saver.o \
				$(OBJDIR)/monitor.o \
				$(OBJDIR)/saver.o \
				$(OBJS_DDS)

OBJS_TEST_DDS 		= $(OBJDIR)/test_dds.o \
					$(OBJS_DDS)

OBJS_TEST_LOSS_RATE = $(OBJDIR)/test_loss_rate.o \
					$(OBJS_DDS)

OBJS_TEST_MEASURE   = $(OBJDIR)/test_measure.o \
					$(OBJS_DDS)

OBJS_TEST_SAVER     = $(OBJDIR)/test_saver.o \
					$(OBJDIR)/saver.o \
					$(OBJDIR)/monitor.o \
					$(OBJS_DDS)

BIN           = testbed_unittest
BIN_DDS       = $(BIN)_dds
BIN_LOST_RATE = $(BIN)_loss_rate
BIN_MEASURE   = $(BIN)_measure
BIN_SAVER     = $(BIN)_saver

all: $(PWD)/$(BIN) data test

$(PWD)/$(BIN): $(OBJS)
	$(LINK.cc) $(OBJS) $(LDLIBS) $(OUTPUT)

$(PWD)/$(BIN_DDS): $(OBJS_TEST_DDS)
	$(LINK.cc) $(OBJS_TEST_DDS) $(LDLIBS) $(OUTPUT)

$(PWD)/$(BIN_LOST_RATE): $(OBJS_TEST_LOSS_RATE)
	$(LINK.cc) $(OBJS_TEST_LOSS_RATE) $(LDLIBS) $(OUTPUT)

$(PWD)/$(BIN_MEASURE): $(OBJS_TEST_MEASURE)
	$(LINK.cc) $(OBJS_TEST_MEASURE) $(LDLIBS) $(OUTPUT)

$(PWD)/$(BIN_SAVER): $(OBJS_TEST_SAVER)
	$(LINK.cc) $(OBJS_TEST_SAVER) $(LDLIBS) $(OUTPUT)

$(OBJDIR)/test_monitor.o: test_monitor.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) test_monitor.cpp

$(OBJDIR)/test_loader.o: test_loader.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) test_loader.cpp

$(OBJDIR)/test_dds.o: test_dds.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) test_dds.cpp

$(OBJDIR)/test_loss_rate.o: test_loss_rate.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) test_loss_rate.cpp

$(OBJDIR)/test_measure.o: test_measure.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) test_measure.cpp

$(OBJDIR)/test_saver.o: test_saver.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) test_saver.cpp

$(OBJDIR)/monitor.o: ../src/Monitor.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) ../src/Monitor.cpp

$(OBJDIR)/loader.o: ../src/Loader.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) ../src/Loader.cpp

$(OBJDIR)/saver.o: ../src/Saver.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) ../src/Saver.cpp

$(OBJDIR)/ddsentitymanager.o: ../src/DDSEntityManager.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) ../src/DDSEntityManager.cpp

$(OBJDIR)/measure_receiver.o: ../src/MeasureReceiver.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) ../src/MeasureReceiver.cpp

$(OBJDIR)/measure_sender.o: ../src/MeasureSender.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) ../src/MeasureSender.cpp

$(OBJDIR)/receiver.o: ../src/Receiver.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) ../src/Receiver.cpp

$(OBJDIR)/sender.o: ../src/Sender.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) ../src/Sender.cpp

$(OBJDIR)/runner.o: ../src/Runner.cpp
	$(MKDIR) $(OBJDIR)
	$(COMPILE.cc) $(OUTPUT) ../src/Runner.cpp

.PHONY: data
data:
	$(CP) $(TESTDATADIR) $(PWD)/
	$(MKDIR) $(REPORTDIR)

test: data $(PWD)/$(BIN)
	cd $(PWD) && LD_LIBRARY_PATH=$(LD_LIB_PATH) ./$(BIN)

test_dds: data $(PWD)/$(BIN_DDS)
	cd $(PWD) && LD_LIBRARY_PATH=$(LD_LIB_PATH) ./$(BIN_DDS)

test_loss_rate: data $(PWD)/$(BIN_LOST_RATE)
	cd $(PWD) && LD_LIBRARY_PATH=$(LD_LIB_PATH) ./$(BIN_LOST_RATE)

test_measure: data $(PWD)/$(BIN_MEASURE)
	cd $(PWD) && LD_LIBRARY_PATH=$(LD_LIB_PATH) ./$(BIN_MEASURE)

test_saver: data $(PWD)/$(BIN_SAVER)
	cd $(PWD) && LD_LIBRARY_PATH=$(LD_LIB_PATH) ./$(BIN_SAVER)
