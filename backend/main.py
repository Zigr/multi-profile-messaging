from fastapi import FastAPI
from routers import profile, template, list_manager, logs

app = FastAPI()
app.include_router(profile.router, prefix="/profiles")
app.include_router(template.router, prefix="/templates")
app.include_router(list_manager.router, prefix="/lists")
app.include_router(logs.router, prefix="/logs")
