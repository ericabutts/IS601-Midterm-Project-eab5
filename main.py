from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.calculator import Calculator
from app.operations import AddOperation

print("Calculator imported:", Calculator)
print("AddOperation imported:", AddOperation)


app = FastAPI()

# Optional: allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create calculator instance
calc = Calculator()

@app.get("/add")
def api_add(a: float, b: float):
    calc.set_operation(AddOperation())
    result = calc.perform_operation(a, b)
    return {"result": float(result)}

# CLI REPL (optional)
if __name__ == "__main__":
    from app.calculator_repl import calculator_repl
    calculator_repl()
