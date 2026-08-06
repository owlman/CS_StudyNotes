# Version 1

# out/calc: calc/main.c calc/getch.c calc/getop.c calc/stack.c
# 	gcc calc/main.c calc/getch.c calc/getop.c calc/stack.c -o out/calc

# Version 2

# cc = gcc
# prom = out/calc
# src = calc/main.c calc/getch.c calc/getop.c calc/stack.c

# $(prom): $(src)
# 	$(cc) $(src) -o $(prom)

# Version 3

# cc = gcc
# prom = out/calc
# deps = calc/calc.h
# obj = out/main.o out/getch.o out/getop.o out/stack.o

# $(prom): $(obj)
# 	$(cc) $(obj) -o $(prom)

# out/main.o: calc/main.c $(deps)
# 	$(cc) -c calc/main.c -o out/main.o

# out/getch.o: calc/getch.c $(deps)
# 	$(cc) -c calc/getch.c -o out/getch.o

# out/getop.o: calc/getop.c $(deps)
# 	$(cc) -c calc/getop.c -o out/getop.o

# out/stack.o: calc/stack.c $(deps)
# 	$(cc) -c calc/stack.c -o out/stack.o

# Version 4

# cc = gcc
# prom = out/calc
# deps = calc/calc.h
# obj = out/main.o out/getch.o out/getop.o out/stack.o

# $(prom): $(obj)
# 	$(cc) -o $(prom) $(obj)

# out/%.o: calc/%.c $(deps)
# 	$(cc) -c $< -o $@

# .PHONY: clean
# clean:
# 	rm -rf $(obj) $(prom)

# Version 5 （修正版：$(wildcard) 接 glob，不是 find 的 -name）

cc = gcc
prom = out/calc
deps = $(wildcard calc/*.h)
src = $(wildcard calc/*.c)
obj = $(src:calc/%.c=out/%.o)

$(prom): $(obj)
	$(cc) -o $(prom) $(obj)

out/%.o: calc/%.c $(deps)
	$(cc) -c $< -o $@

.PHONY: clean
clean:
	-rm -f $(obj) $(prom)
