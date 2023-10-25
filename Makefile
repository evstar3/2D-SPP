SRCDIR=src
OBJDIR=obj
INCDIR=include

CC=gcc
CFLAGS=-c -Iinclude -Wall -std=gnu99
LD=gcc
LDFLAGS=

SOURCES=$(addprefix $(SRCDIR)/, packer.c problem.c strip.c box.c)
HEADERS=$(addprefix $(INCDIR)/, packer.h problem.h strip.h box.h)

OBJS:=$(patsubst $(SRCDIR)/%.c, $(OBJDIR)/%.o, $(SOURCES))

TARGET=packer

all: $(TARGET)

$(TARGET): $(OBJS) $(HEADERS)
	$(LD) $(LDFLAGS) -o $@ $^

$(OBJS): $(OBJDIR)/%.o: $(SRCDIR)/%.c $(HEADERS)
	$(CC) $(CFLAGS) -o $@ $<

$(OBJS): | $(OBJDIR)
$(OBJDIR):
	mkdir -p $@

.PHONY: clean
clean:
	rm -rf $(OBJDIR) $(TARGET)

.SUFFIXES: