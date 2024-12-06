FROM python:3.13.1 AS builder

WORKDIR /app

# Install PDM
RUN pip install pdm

# Copy project files (including pyproject.toml and pdm.lock)
COPY pyproject.toml pdm.lock ./
COPY src/ ./src/

# Install dependencies
RUN pdm sync --no-self --prod

# Stage 2: Final image
FROM python:3.13.1-slim

WORKDIR /app

# Copy dependencies from the builder stage
#COPY --from=builder /app/__pypackages__/3.13/lib/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /app/.venv/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/

# Copy your application code
COPY src/ ./src/

# Set the entry point for your application
CMD ["python", "src/main.py"]
