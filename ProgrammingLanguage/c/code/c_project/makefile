cc = gcc
prom = calc
deps = $(shell find ./ -name "*.h")
src = $(shell find ./ -name "*.c")
obj = $(src:%.c=%.o) 

$(prom): $(obj)
	$(CC) -o $(prom) $(obj)

%.o: %.c $(deps)
	$(CC) -c $< -o $@

clean:
	rm -rf $(obj) $(prom)