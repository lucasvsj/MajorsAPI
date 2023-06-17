try:
    from fastapi import FastAPI
except Exception as e:
    print(f'Error! Some Modules are Missing  : {e}')

from .routers import majors


app = FastAPI()

app.include_router(majors.router)

@app.get('/')
async def root():
    return {"message" : "Hello World"}