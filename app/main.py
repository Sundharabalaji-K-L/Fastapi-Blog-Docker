from fastapi import FastAPI
import blog.routers as blog_routers
import auth.routers as auth_routers

app = FastAPI()

app.include_router(blog_routers.router)
app.include_router(auth_routers.router)
