.PHONY: check fix docs clean

HATCH = hatch

check:
	$(HATCH) $(HATCHFLAGS) fmt --check
	$(HATCH) $(HATCHFLAGS) run types:check
	$(HATCH) $(HATCHFLAGS) test

fix:
	$(HATCH) $(HATCHFLAGS) fmt

docs:
	$(HATCH) $(HATCHFLAGS) run docs:build

clean:
	$(HATCH) $(HATCHFLAGS) env prune
	$(RM) -r docs/_build/
