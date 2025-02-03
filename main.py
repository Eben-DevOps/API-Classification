from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import requests
from functools import lru_cache
from typing import Union

app = FastAPI(title="Number Classification API")

# Enable CORS for all origins (development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for serving static files like favicon.ico.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint with a welcome message.
@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Number Classification API! Use /api/classify-number?number=<number> to classify a number."
    }

# Favicon endpoint to serve the favicon.ico file.
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

# Cache results for repeated inputs to improve speed.
@lru_cache(maxsize=1000)
def calculate_digit_sum(n: int) -> int:
    return sum(int(digit) for digit in str(abs(n)))

@lru_cache(maxsize=1000)
def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return n == sum(d ** power for d in digits)

@lru_cache(maxsize=1000)
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

@lru_cache(maxsize=1000)
def is_perfect(n: int) -> bool:
    if n <= 1:
        return False
    divisors_sum = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            divisors_sum += i
            if i != n // i:
                divisors_sum += n // i
        i += 1
    return divisors_sum == n

def fetch_fun_fact(n: Union[int, float]) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "No fun fact available.")
        else:
            return "No fun fact available."
    except requests.Timeout:
        return "Fun fact request timed out."
    except Exception:
        return "Error fetching fun fact."

@app.get("/api/classify-number")
async def classify_number(
    number: str = Query(..., description="The number to classify", example="371")
):
    try:
        # Try to convert the input to a float (handles integers and floating-point numbers)
        num = float(number)
    except ValueError:
        # If conversion fails, return a 400 error with the invalid input
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "Invalid input. Please provide a valid number.",
                "number": number
            }
        )

    # Calculate properties
    armstrong = is_armstrong(int(num)) if num.is_integer() else False
    prime = is_prime(int(num)) if num.is_integer() else False
    perfect = is_perfect(int(num)) if num.is_integer() else False
    digit_sum = calculate_digit_sum(int(num)) if num.is_integer() else None
    parity = "even" if num % 2 == 0 else "odd" if num.is_integer() else None

    properties = ["armstrong"] if armstrong else []
    if parity:
        properties.append(parity)

    fun_fact = fetch_fun_fact(num)

    return JSONResponse(
        content={
            "status": "success",
            "message": "The input is valid.",
            "number": num,
            "is_prime": prime,
            "is_perfect": perfect,
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        },
        status_code=200
    )