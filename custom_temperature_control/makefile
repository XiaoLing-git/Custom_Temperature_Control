ifeq ($(OS),Windows_NT)
    # Windows系统配置
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
SUB_FOLDER :=


clean_cache:
ifeq ($(DETECTED_OS),Windows)
	if exist "$(CURRENT_DIR)__pycache__" ($(RMDIR) "$(CURRENT_DIR)__pycache__")
else
	$(RM) "$(CURRENT_DIR)$(SEP)__pycache__"
endif



clean:clean_cache
ifeq ($(DETECTED_OS),Windows)
#	clean next level folder
	@for %%d in ($(SUB_FOLDER)) do ( \
		make -C "$(CURRENT_DIR)%%d" clean || exit 1; \
	)

else
#	clean next level folder
	@for dir in $(SUB_FOLDER); do \
        make -C "$(CURRENT_DIR)$(SEP)$$dir" clean || exit 1; \
    done

endif
