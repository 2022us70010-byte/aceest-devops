# ACEest Fitness & Gym — DevOps CI/CD Pipeline

A Flask-based REST API for fitness and gym management, built with full
DevOps automation including Git version control, Docker containerization,
Jenkins BUILD integration, and GitHub Actions CI/CD.

## Local Setup

1. Clone the repository:
   git clone https://github.com/2022us70010-byte/aceest-devops
   cd aceest-devops

2. Install dependencies:
   pip install -r requirements.txt

3. Run the application:
   python app.py

4. Visit: http://localhost:5000

## Running Tests Manually

   pytest test_app.py -v

## Docker

   docker build -t aceest-fitness .
   docker run -p 5000:5000 aceest-fitness

## Jenkins Integration

Jenkins is configured as a Freestyle project that pulls from GitHub and
runs pip install, pytest, and docker build as the BUILD phase. This
validates that all code integrates cleanly in a controlled environment.

## GitHub Actions

The .github/workflows/main.yml pipeline triggers on every push/PR to main
and runs three sequential jobs:
- Build & Lint: installs dependencies and checks syntax with flake8
- Docker Image Assembly: builds the Docker image successfully
- Automated Testing: runs the full pytest suite both locally and inside
  the Docker container