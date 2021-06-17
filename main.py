import fastapi
import uvicorn

api = fastapi.FastAPI()

@api.get('/api/calculate')
def calculate():
    return 2 + 2


uvicorn.run(api, host="127.0.0.1", port=8000)
