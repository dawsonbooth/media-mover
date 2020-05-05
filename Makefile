VERSION := $(shell poetry version | grep -oE '[^ ]+$$')

PLATFORM :=
ifeq ($(OS),Windows_NT)
	PLATFORM = win32
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		PLATFORM = linux
	endif
	ifeq ($(UNAME_S),Darwin)
		PLATFORM = darwin
	endif
endif

BUILDFLAGS = --onefile --name media-mover-$(VERSION)-$(PLATFORM) #--windowed

all: list

list:
	@sh -c "$(MAKE) -p no_targets__ | \
		awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {\
			split(\$$1,A,/ /);for(i in A)print A[i]\
		}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"

clean:
	rm -rf build/ dist/
	rm -f *.spec

build:
	pyinstaller $(BUILDFLAGS) media-mover.py
	

