TARGET_ARCH = linux

CC     = g++
OPT    = -O3 -Wno-deprecated
DEBUG  = -g
OTHER  = 
CFLAGS = $(OPT) $(OTHER)
# CFLAGS = $(DEBUG) $(OTHER)

MODULE = example
SRCS = main.cpp test_fixture.cpp example.cpp
OBJS = $(SRCS:.cpp=.o)

include ../Makefile.defs
