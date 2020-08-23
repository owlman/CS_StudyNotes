###############################################################
#   author: lingjie                                           #
#   time  : 2016-5-18                                         #
###############################################################
outdir = Debug
src = $(shell find ./ -name "*.cpp")
obj = $(src:%.cpp=$(outdir)/%.o) 
dephead = $(shell find ./ -name "*.h")
prom = $(outdir)/test.exe
cc = g++
cflgs = -Wall -g 

all: outdir $(prom) 
outdir:
	if [ ! -x "$(outdir)" ]; then \
		mkdir $(outdir);          \
		if [ ! -x "$(outdir)/algorithm" ]; then \
			mkdir $(outdir)/algorithm;\
		fi \
	fi
	
$(prom): $(obj) 
	$(cc)  $(obj) -o $(prom) $(cflgs)  

$(outdir)/%.o: ./%.cpp $(dephead)
	$(cc) -c $< -o $@ $(cflgs)

clean: 
	rm -rf $(obj) $(prom) $(outdir)
