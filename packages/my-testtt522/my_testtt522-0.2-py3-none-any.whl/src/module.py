import uvicorn
from fastapi import FastAPI

app = FastAPI()
def main():
    print("Hello from my_testtt52!")
@app.get("/sum")
async def sum(a: int, b: int):
    return {
        "sum": a + b
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    main()