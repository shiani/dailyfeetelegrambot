# Use a lightweight Python base image
FROM python:3.9-slim

# Install necessary dependencies
RUN pip install requests pyTelegramBotAPI jdatetime pytz

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY dailyfee.py /app

# Command to run the Python script
CMD ["python", "dailyfee.py"]
