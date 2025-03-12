# Pull base image
FROM python:3.12.3-slim-bullseye


# Install build dependencies b/c the base image lacks
RUN apt-get update && apt-get install -y \
    curl\
    build-essential \
    libpq-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set global environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/usr/src/app



# Set environment variables for Poetry installation
ENV POETRY_VERSION=1.8.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1


# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${POETRY_HOME}/bin:$PATH"

# Set the working directory
WORKDIR $APP_HOME

# Create a user to run the application
RUN addgroup --system app && adduser --system --group app

# Create the static and media files directories
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

# Copy the lockfile and pyproject file first to leverage Docker layer caching
COPY pyproject.toml poetry.lock ./

# Install only development dependencies by default
ARG ENVIRONMENT=development
RUN poetry install --no-root --only $ENVIRONMENT
RUN poetry add psycopg2

# Copy the rest of the application code
# This should be always after dependency installation
# to protect reinstalling dependencies in every code change
COPY . .

# change the ownership all the files to the app user
RUN chown -R app:app $APP_HOME

EXPOSE 8000