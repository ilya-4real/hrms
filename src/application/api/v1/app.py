from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import HTMLResponse
from config.settings import AppSettings
from fastapi.templating import Jinja2Templates
from application.api.v1.departments.router import router as dep_router
from config.contanier import container
from dishka.integrations.fastapi import setup_dishka
from application.api.v1.employees.router import router as empl_router


def get_app() -> FastAPI:
    settings = AppSettings()  # pyright: ignore
    app = FastAPI(
        debug=settings.DEBUG,
        title="HR managent system",
        description="System that helps HRs to do their job",
        default_response_class=HTMLResponse,
    )
    app.include_router(router)
    app.include_router(dep_router)
    app.include_router(empl_router)

    setup_dishka(container, app)
    return app


templates = Jinja2Templates(directory="src/templates")

router = APIRouter(tags=["index"])


@router.get("/", status_code=status.HTTP_200_OK, description="returns root html page")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html")
