.PHONY: all
all: tools.stamp
	@true

tools.stamp:
	$(info doing [$@])
	@templar_cmd install_deps
	@make_helper touch-mkdir $@

.PHONY: clean
clean:
	@git clean -qffxd
