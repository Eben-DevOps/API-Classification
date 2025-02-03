# Number Classification API

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Local Development](#local-development)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [License](#license)

## Features

- **Number Classification:**  
  - Armstrong number check
  - Prime number check
  - Perfect number check
  - Digit sum calculation
  - Odd or even classification
- **Fun Fact Integration:**  
  - Retrieves math facts from Numbers API
- **CORS Enabled:**  
  - Supports cross-origin requests
- **Static File Handling:**  
  - Serves favicon
- **Deployment Ready:**  
  - Configured for Vercel with `vercel-asgi`

## Tech Stack

- **Python 3.8+**
- **FastAPI**
- **Uvicorn**
- **Requests**
- **Docker**

## Project Structure

- **main.py:** API logic and endpoints
- **static/favicon.ico:** Favicon file
- **requirements.txt:** Dependencies
- **Dockerfile:** Build instructions

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Healerkay/HNG-Devops-Task  
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   ```

   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Local Development

Ensure you have the static directory and a favicon.ico file in it.

Run the application using Uvicorn:
```bash
uvicorn main:app --reload
```

## Access the API

- Root endpoint: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- API endpoint: [http://127.0.0.1:8000/api/classify-number?number=371](http://127.0.0.1:8000/api/classify-number?number=371)
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

