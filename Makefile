# MATLAB configuration
MEX    ?= mex
MEXEXT ?= $(shell mexext)

SRCS = dellipse.cpp dellipsoid.cpp dsegment.cpp trisurfupd.cpp
OBJS = $(SRCS:.cpp=.$(MEXEXT))

%.$(MEXEXT): %.cpp
	$(MEX) -largeArrayDims $< -lmwlapack

all: $(OBJS)

purge:
	-rm -f $(OBJS)

.PHONY: all clean purge
