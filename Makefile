install:
	@echo "** $(good)Installing packages...$(clear) **"
	pip3 install poetry
	poetry install
	@echo "**$(good)Installing espeak...$(clear) **"
	sudo apt install espeak
	@echo ""
	@echo "** $(good)Done! Use poetry run python3 dotloot.py filters/example.yaml to run the example filter.$(clear) **"
