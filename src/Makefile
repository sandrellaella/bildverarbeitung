MACOSX_32_VIGRA_BIN_DIR = /opt/local32/bin
MACOSX_32_CXXFLAGS = -I. `$(MACOSX_32_VIGRA_BIN_DIR)/vigra-config --cppflags` -O3 -arch i386
MACOSX_32_LDFLAGS  = `$(MACOSX_32_VIGRA_BIN_DIR)/vigra-config --libs` `$(MACOSX_32_VIGRA_BIN_DIR)/vigra-config --fftw-lib` `$(MACOSX_32_VIGRA_BIN_DIR)/pkg-config --libs opencv` -bundle -undefined dynamic_lookup -arch i386

MACOSX_VIGRA_BIN_DIR = /opt/local/bin
MACOSX_CXXFLAGS = -I. `$(MACOSX_VIGRA_BIN_DIR)/vigra-config --cppflags` -O3
MACOSX_LDFLAGS  = `$(MACOSX_VIGRA_BIN_DIR)/vigra-config --libs` `$(MACOSX_VIGRA_BIN_DIR)/vigra-config --fftw-lib` `$(MACOSX_VIGRA_BIN_DIR)/pkg-config --libs opencv` -bundle -undefined dynamic_lookup

LINUX_VIGRA_BIN_DIR = /informatik/home/seppke/libs/vigra/bin
LINUX_CXXFLAGS = -I. `$(LINUX_VIGRA_BIN_DIR)/vigra-config --cppflags` `pkg-config --cflags opencv` -O3 
LINUX_LDFLAGS  = `$(LINUX_VIGRA_BIN_DIR)/vigra-config --libs`  `$(LINUX_VIGRA_BIN_DIR)/vigra-config --fftw-lib` `pkg-config --libs opencv`  -shared -fPIC 


all: macosx

macosx_python-wrapper.o: 
	g++ $(MACOSX_CXXFLAGS) -c python-wrapper.cxx


macosx:	macosx_python-wrapper.o
	g++ $(MACOSX_LDFLAGS) python-wrapper.o -o libpython-wrapper.dylib
	cp libpython-wrapper.dylib libpython-wrapper.so


linux_python-wrapper.o:	
	gg++ $(LINUX_CXXFLAGS) -c python-wrapper.cxx

linux:	linux_python-wrapper.o
	g++ $(LINUX_LDFLAGS) python-wrapper.o -o libpython-wrapper.so

install:
	cp libpython-wrapper.dylib ..
	cp libpython-wrapper.so ..

clean:
	rm *.o
	rm *.so
	rm *.dylib

