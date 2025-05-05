FROM python:3.13-alpine

# Create app directory
WORKDIR /app

# Copy the entire src directory to preserve your project structure
COPY src/ /app/src/

# Make sure the Python files are executable
RUN chmod +x /app/src/compiler/*.py

# Set PYTHONPATH before using it
ENV PYTHONPATH=/app/src

# Add the current PYTHONPATH to the new PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:${PYTHONPATH}"

# Create a directory for user code
RUN mkdir /app/code

# Set the working directory to where user code will be mounted
WORKDIR /app/code

# Create an entry point script
RUN echo '#!/bin/bash\npython /app/src/compiler/main.py "$@"' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# The entrypoint executes the main.py script
ENTRYPOINT ["/app/entrypoint.sh"]

# Default argument if none is provided
CMD ["--help"]
