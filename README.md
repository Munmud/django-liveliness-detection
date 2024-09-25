# Liveliness Detection: Eye Blink Using Django and Docker

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Running with Docker](#running-with-docker)

---

## Introduction

Liveliness detection is an essential component in biometric authentication systems, verifying that a user is physically present during the authentication process. This project implements eye blink detection using Django for the backend and Docker for containerization, making it easier to deploy and manage dependencies.

## Features

- Real-time eye blink detection using webcam input.
- User-friendly web interface built with Django.
- Ability to save and analyze detection results.
- Support for multiple users.
- Easy setup and deployment with Docker.

## Requirements

To run this project, you will need:

- Docker and Docker Compose
- A compatible web browser

## Installation

### Step-by-Step Installation

1. **Clone the repository:**
```bash
 git clone https://github.com/Munmud/django-liveliness-detection
 cd django-liveliness-detection
```

## Running with Docker

1. **Build and Run the Docker Container:**
Use the following command to build and run your Docker container:
```bash
docker-compose up --build
```

2. **Access the Application:**
Once the container is running, you can access the application in your web browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

3. **Stopping the Container:**
To stop the running container, you can use:
```bash
docker-compose down
```
