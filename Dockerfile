FROM python:3.8-alpine

# Set the working directory
WORKDIR /function

# Copy your function code
COPY . .

# Install any dependencies (if you have any)
# RUN pip install -r requirements.txt

# Specify the command to run the function
CMD ["python", "-m", "nuclio"]
