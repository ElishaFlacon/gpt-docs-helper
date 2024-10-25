import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from core.ai import AI


ai = AI()
ai.extract_documents()

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/query/")
async def run_query_endpoint(query: str = Form(...)):
    if query == "":
        return JSONResponse(content={"message": "Invalid query"}, status_code=400)

    response = ai.query(query)

    return {"answer": response}


app.mount("/", StaticFiles(directory="templates", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
