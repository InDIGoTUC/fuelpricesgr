FROM python:3.11-bookworm

WORKDIR /code

# Install tzdata and cron
RUN apt -qq update && apt -qq install -y curl cron tzdata

# Set the timezone to Greece (Europe/Athens)
ENV TZ=Europe/Athens
RUN ln -snf /usr/share/zoneinfo/Europe/Athens /etc/localtime && echo "Europe/Athens" > /etc/timezone

# Copy poetry files and install dependencies
COPY poetry.lock pyproject.toml ./
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN POETRY_VIRTUALENVS_CREATE=false /root/.local/bin/poetry install

# Copy application code
COPY ./fuelpricesgr /code/fuelpricesgr

# Copy any necessary configuration files
# COPY ./var/ /code/var

# Use the full path to python in the cron job
RUN echo "30 08 * * * cd /code && /usr/local/bin/python -m fuelpricesgr.commands.import --verbose --types DAILY_COUNTRY,DAILY_PREFECTURE --start-date 2024-09-17 >> /var/log/cron.log 2>&1" > /etc/cron.d/fuelpricesgr_cron

# Set correct permissions for the cron file
RUN chmod 0644 /etc/cron.d/fuelpricesgr_cron

# Apply the cron job
RUN crontab /etc/cron.d/fuelpricesgr_cron

# Create log file
RUN touch /var/log/cron.log

# Initial Database Population
RUN python -m fuelpricesgr.commands.import --verbose --types DAILY_COUNTRY,DAILY_PREFECTURE --start-date 2024-09-17

# Start the cron service in the background and ensure both processes are properly managed using JSON format
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log & uvicorn fuelpricesgr.main:app --host 0.0.0.0 --port 8000"]