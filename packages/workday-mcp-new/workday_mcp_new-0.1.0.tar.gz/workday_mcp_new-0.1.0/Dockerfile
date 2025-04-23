FROM python:3.13-alpine

# Install system dependencies
RUN apk add --no-cache gcc musl-dev linux-headers curl

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install uv and verify its location
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    find / -name uv -type f 2>/dev/null && \
    ls -la /root/.cargo/bin || echo "Cargo bin doesn't exist"

# Add uv to PATH and verify installation
RUN export PATH="$HOME/.cargo/bin:$PATH" && \
    which uv || echo "uv not in PATH" && \
    ls -la $HOME/.cargo/bin || echo "No cargo bin found" 

# Use pip instead of uv for reliability
RUN pip install --upgrade pip && \
    pip install -e .

# Run the application with Python directly
CMD ["python", "-m", "workday_mcp_new"]