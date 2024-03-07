FROM python:3.9

WORKDIR /code

# Install Python dependencies
COPY ./utils /code/utils

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r /code/requirements.txt

# Copy the rest of the application code
COPY . /code/app

EXPOSE 5000

# RUN useradd -m myuser
# USER myuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
