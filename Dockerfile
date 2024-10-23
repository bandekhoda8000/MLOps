FROM python:3.8-alpine

# Install necessary packages for Nuclio
RUN apk add --no-cache \
        bash \
        build-base \
        libffi-dev \
        openssl-dev \
        py3-pip \
        curl \
        libstdc++ \
        linux-headers \
        musl-dev \
        gcc

# Set the working directory
WORKDIR /function

# Copy your function code
COPY . .

# Install any dependencies (if you have any)
# RUN pip install -r requirements.txt

# Specify the command to run the function
CMD ["python", "-m", "nuclio"]
