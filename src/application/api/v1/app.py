from application.api.v1.departments.router import router as dep_router
from application.api.v1.employees.router import router as empl_router
from application.api.v1.events.router import router as events_router
from config.contanier import container
from config.settings import AppSettings
from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


def get_app() -> FastAPI:
    # static_files = StaticFiles(directory="./static")
    settings = AppSettings()  # pyright: ignore
    app = FastAPI(
        debug=settings.DEBUG,
        title="HR managent system",
        description="System that helps HRs to do their job",
        default_response_class=HTMLResponse,
    )
    # app.mount("/static", static_files, name="static")
    app.include_router(router)
    app.include_router(dep_router)
    app.include_router(empl_router)
    app.include_router(events_router)
    setup_dishka(container, app)
    return app


templates = Jinja2Templates(directory="src/templates")

router = APIRouter(tags=["index"])


@router.get("/", status_code=status.HTTP_200_OK, description="returns root html page")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html")
