# YouTube Summarizer API

## Overview

A FastAPI-based application that summarizes YouTube video transcripts.

## Features

- Extracts transcripts from YouTube videos.
- Generates summaries of video content.
- Provides API endpoints for integration.

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/youtube_summarizer.git
   cd youtube_summarizer
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   - Create a `.env` file in the `youtube_summarizer` directory (`deep_alpha/youtube_summarizer/.env`) and populate it with necessary variables.

5. **Run the Application Locally:**

   ```bash
   uvicorn app.main:app --reload
   ```

6. **Run Tests:**

   ```bash
   pytest
   ```

7. **Run with Docker Compose:**

   Ensure you have Docker installed. If Docker is not installed, follow the instructions below to install Docker for your operating system.

   ### Installing Docker

   **For Windows:**
   
   1. **Download Docker Desktop:**
      - Visit [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop).
      - Click on **Download for Windows**.

   2. **Install Docker Desktop:**
      - Run the downloaded installer and follow the on-screen instructions.
      - During installation, ensure that the option to use WSL 2 instead of Hyper-V is selected for better performance.

   3. **Start Docker Desktop:**
      - After installation, launch Docker Desktop.
      - Follow any additional setup prompts.

   4. **Verify Installation:**
      - Open Command Prompt and run:
        ```bash
        docker --version
        docker compose version
        ```

   **For macOS:**
   
   1. **Download Docker Desktop:**
      - Visit [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop).
      - Click on **Download for Mac**.

   2. **Install Docker Desktop:**
      - Open the downloaded `.dmg` file and drag Docker to the Applications folder.
      - Launch Docker from the Applications folder.

   3. **Verify Installation:**
      - Open Terminal and run:
        ```bash
        docker --version
        docker compose version
        ```

   **For Linux:**
   
   1. **Update Package Index:**
      ```bash
      sudo apt-get update
      ```

   2. **Install Docker Engine:**
      ```bash
      sudo apt-get install docker.io
      ```

   3. **Start and Enable Docker:**
      ```bash
      sudo systemctl start docker
      sudo systemctl enable docker
      ```

   4. **Verify Installation:**
      ```bash
      docker --version
      docker compose version
      ```

   ### Running Docker Compose

   Once Docker is installed and verified, navigate to the project directory and run:

   ```bash
   docker compose up --build
   ```

   > **Note:** Use `docker compose` (with a space) instead of `docker-compose` to align with the latest Docker CLI standards.

## Deployment

Details on deploying the application using Docker and your preferred cloud provider.

## API Documentation

Accessible at `/docs` once the application is running.

## License

MIT License
