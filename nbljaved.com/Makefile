# Makefile for building and publishing nbljaved.com blog

# Variables
EMACS = emacs
PUBLISH_FILE = publish.el
SOURCE_DIR = org
OUTPUT_DIR = html

# Default target
.PHONY: all clean build help

all: rebuild

# Build the site
build:
	@echo "Building the blog..."
	$(EMACS) -Q --batch --load $(PUBLISH_FILE) --eval "(org-publish-all t)"
	@echo "Blog built successfully in $(OUTPUT_DIR)/"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	trash $(OUTPUT_DIR)/*
	@echo "Clean complete."

# Rebuild from scratch
rebuild: clean build

# Start local server (if you have a simple HTTP server)
serve: build
	@echo "Starting local server on http://localhost:8000"
	cd $(OUTPUT_DIR) && python3 -m http.server 8000

# Show help
help:
	@echo "Available targets:"
	@echo "  all     - Build the site (default)"
	@echo "  build   - Build the site using org-publish"
	@echo "  clean   - Remove generated files"
	@echo "  rebuild - Clean and rebuild"
	@echo "  serve   - Build and start local server"
	@echo "  help    - Show this help message"
