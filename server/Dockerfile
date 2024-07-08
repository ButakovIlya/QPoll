FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory
WORKDIR /app

# Copy the requirements file separately to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Install system dependencies
RUN apt-get update --allow-unauthenticated \
    && apt-get install -y python3-dev mariadb-client build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies, including MySQL Connector
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . /app/

# Run migrations
RUN python manage.py makemigrations

# Apply migrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
# EXPOSE 8000
EXPOSE 9000

# Run Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "9000", "qpoll.asgi:application"]
# ENTRYPOINT ["gunicorn", "qpoll.wsgi", "-b", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "qpoll.wsgi:application"]
