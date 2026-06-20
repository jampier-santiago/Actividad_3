from fastapi import FastAPI

app = FastAPI(title="K8s Demo Service")

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/info")
def info():
    return {
        "service": "k8s-demo",
        "version": "1.0.0",
        "description": "Microservicio demo para trabajo K8S"
    }