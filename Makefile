### Variables generiques
CC=clang # compilateur
CFLAGS=-I. -W -Wall -g -MMD # warnings + dependances
EXTRA_CFLAGS= # aucune pour ce projet
EXTRA_LDFLAGS=# aucune pour ce projet

### Variables liées à la compilation des sources
EXEC=somb	# ./structures pour executer
SRC=$(wildcard *.c)	# Tous les fichiers .c
OBJ=$(subst $(src),$(src),$(SRC:.c=.o))	# *.c --> *.o
DEP=$(SRC:.c=.d)	# *.c --> *.d

### Cibles de compilation
default: $(EXEC)

#### Construction de l'executable
$(EXEC): $(OBJ)
	$(CC) $^ $(EXTRA_LDFLAGS) -o $@

#### Construction generique des fichiers .o
.c.o:
	$(CC) $(CFLAGS) -c $<

### Inclusion des dependances
-include $(DEP)

### Nettoyage du repertoire
.PHONY: clean
clean:
	@rm -rf $(EXEC) $(OBJ) $(DEP)

.PHONY: mem
mem:
	valgrind ./$(EXEC) -b ../files/airbnb* ../files/test.txt
