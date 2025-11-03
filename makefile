ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    RM := del /Q /F
    RMDIR := rmdir /Q /S
    MKDIR := mkdir
    EXE_EXT := .exe
    SEP := \\
    CURRENT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
else
    DETECTED_OS := Linux
    RM := rm -rf
    RMDIR := rm -rf
    MKDIR := mkdir -p
    EXE_EXT :=
    SEP := /
    CURRENT_DIR := $(CURDIR)
endif


RUN := poetry run
PRECOMMIT := pre-commit run
SUB_FOLDER := custom_temperature_control test


clean_cache:
ifeq ($(DETECTED_OS),Windows)
	if exist "$(CURRENT_DIR).mypy_cache" ($(RMDIR) "$(CURRENT_DIR).mypy_cache")
	if exist "$(CURRENT_DIR)__pycache__" ($(RMDIR) "$(CURRENT_DIR)__pycache__")
else
	$(RM) "$(CURRENT_DIR)$(SEP).mypy_cache"
	$(RM) "$(CURRENT_DIR)$(SEP)__pycache__"
endif


clean:clean_cache
ifeq ($(DETECTED_OS),Windows)
	if exist "$(CURRENT_DIR)build" ($(RMDIR) "$(CURRENT_DIR)build")
	if exist "$(CURRENT_DIR)dist" ($(RMDIR) "$(CURRENT_DIR)dist")

#	clean next level folder
	@for %%d in ($(SUB_FOLDER)) do ( \
		make -C "$(CURRENT_DIR)%%d" clean || exit 1; \
	)

else
	$(RMDIR) "$(CURRENT_DIR)$(SEP)build"
	$(RMDIR) "$(CURRENT_DIR)$(SEP)dist"

#	clean next level folder
	@for dir in $(SUB_FOLDER); do \
        make -C "$(CURRENT_DIR)$(SEP)$$dir" clean || exit 1; \
    done

endif


shell:
	poetry shell

install:
	poetry install

build:clean
	poetry build

update:
	poetry update

check:
	$(PRECOMMIT) --all-files

commit:clean
	git add .
	git commit -m "$(msg)"

push:commit
	git push

echo:
	echo $1
	echo $2
	echo $2
