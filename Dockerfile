# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
# USER appuser
ARG SECRET_KEY , DEBUG_MODE , REDIS_HOST , REDIS_PORT , DB_NAME , DB_USER , DB_PASSWORD , DB_HOST , DB_PORT
# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000
ENV PORT 8000

# sets django related env keys
RUN export SECRET_KEY=$SECRET_KEY, DEBUG_MODE=$DEBUG_MODE
# sets redis related configs
RUN export REDIS_PORT=$REDIS_PORT, REDIS_HOST=$REDIS_HOST
# sets postgres related configs
RUN export DB_USER=$DB_USER, DB_NAME=$DB_NAME, DB_PASSWORD=$DB_PASSWORD, DB_HOST=$DB_HOST, DB_PORT=$DB_PORT

RUN python manage.py collectstatic --no-input
# Run the application.