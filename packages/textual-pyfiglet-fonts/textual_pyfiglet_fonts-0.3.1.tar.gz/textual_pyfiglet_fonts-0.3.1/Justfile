install:
	uv sync

# Run the script to generate the fonts list.
make-list:
	uv run make_fonts_list.py	

# Build the package, run clean first
build: clean
	@echo "Building the package..."
	uv build

# Publish the package, run build first
publish: build
	@echo "Publishing the package..."
	uv publish

# Remove the build and dist directories
clean:
	@echo "Cleaning the package..."
	rm -rf build dist
	find . -name "*.pyc" -delete

# Remove the virtual environment and lock file
del-env:
	@echo "Deleting the virtual environment..."
	rm -rf .venv
	rm -rf uv.lock

reset: clean del-env install
	@echo "Resetting the environment..."