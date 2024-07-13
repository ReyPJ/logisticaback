FROM python:3.12.3-slim

# Dir

WORKDIR /app

# Copy

COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Envirnment variables
ENV PYTHONDONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Migration and collect static
RUN python manage.py migrate
# Install gunicorn
RUN pip install gunicorn

# Expose port
EXPOSE 8000

# Run server
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api.wsgi:application"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]