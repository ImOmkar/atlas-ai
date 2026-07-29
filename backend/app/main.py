from fastapi import FastAPI


app = FastAPI(title="Atlas AI")

@app.get('/health')
def health():
    return {
        "status": "healthy",
        "application": "Atlas AI"
    }

