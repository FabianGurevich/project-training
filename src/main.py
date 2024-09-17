from fastapi import FastAPI


from src.api.v1.urls import router


app = FastAPI()

app.include_router(router)
