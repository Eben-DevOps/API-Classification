from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
from functools import lru_cache

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

def fetch_fun_fact(n: int) -> str:
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
        num = int(number)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={"number": number, "error": True}
        )
    
    # Calculate properties in parallel (if needed) or sequentially for simplicity.
    armstrong = is_armstrong(num)
    prime = is_prime(num)
    perfect = is_perfect(num)
    digit_sum = calculate_digit_sum(num)
    parity = "even" if num % 2 == 0 else "odd"

    properties = ["armstrong"] if armstrong else []
    properties.append(parity)

    fun_fact = fetch_fun_fact(num)

    return {
        "number": num,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }