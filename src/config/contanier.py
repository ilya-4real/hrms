from typing import AsyncIterable
from dishka import Provider, Scope, provide, make_async_container
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from fastapi.templating import Jinja2Templates

from config.settings import AppSettings
from domain.usecases.department import CreateDeaprtmentUseCase, GetAllDepartmentsUseCase
from domain.usecases.employee import (
    AddEmployeeUseCase,
    GetAllEmployeesUseCase,
    GetEmployeeUsecase,
    GetEmployeesByDepartmentUseCase,
    UpdateEmployeeUsecase,
)
from domain.usecases.event import (
    CreateEventUseCase,
    DeleteEventUsecase,
    GetCurrentEventsUseCase,
    GetEventsHistoryUseCase,
)
from domain.usecases.kpi import GetEmployeesKPIListUseCase
from domain.usecases.stats import GetCompanyStatsUsecase, GetCountByDepartmentUseCase, GetEmployeeStatsUseCase
from gateways.postgres.department import SQLDepartmentGateway
from gateways.postgres.employee import SQLEmployeeGateway
from gateways.postgres.event import SQLEventGateway
from gateways.postgres.kpi import SQLKPIGateway
from gateways.postgres.statsgateway import SQLStatsGateway


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def get_app_settings(self) -> AppSettings:
        return AppSettings()  # type: ignore

    @provide(scope=Scope.APP)
    def get_alchemy_engine(self, settings: AppSettings) -> AsyncEngine:
        return create_async_engine(settings.postgres_dsn, echo=settings.DEBUG)

    @provide(scope=Scope.APP)
    def get_sessionmanker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine)

    @provide(scope=Scope.APP)
    def get_templating(self) -> Jinja2Templates:
        return Jinja2Templates("src/templates")

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_department_gateway(
        self, session: AsyncSession
    ) -> SQLDepartmentGateway:
        return SQLDepartmentGateway(session)

    @provide(scope=Scope.REQUEST)
    async def get_create_department_useacase(
        self, db_session: AsyncSession
    ) -> CreateDeaprtmentUseCase:
        gateway = SQLDepartmentGateway(db_session)
        return CreateDeaprtmentUseCase(gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def get_all_departments_usecase(
        self, db_session: AsyncSession
    ) -> GetAllDepartmentsUseCase:
        gateway = SQLDepartmentGateway(db_session)
        return GetAllDepartmentsUseCase(gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def add_employee_usecase(
        self, db_session: AsyncSession
    ) -> AddEmployeeUseCase:
        gateway = SQLEmployeeGateway(db_session)
        return AddEmployeeUseCase(gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def get_all_employees_usecase(
        self, db_session: AsyncSession
    ) -> GetAllEmployeesUseCase:
        gateway = SQLEmployeeGateway(db_session)
        return GetAllEmployeesUseCase(gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def get_employee_use_case(
        self, db_session: AsyncSession
    ) -> GetEmployeeUsecase:
        gateway = SQLEmployeeGateway(db_session)
        return GetEmployeeUsecase(gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def get_employee_by_dep_usecase(
        self, db_session: AsyncSession
    ) -> GetEmployeesByDepartmentUseCase:
        empl_gateway = SQLEmployeeGateway(db_session)
        dep_gateway = SQLDepartmentGateway(db_session)
        return GetEmployeesByDepartmentUseCase(empl_gateway, dep_gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def update_employee_usecase(
        self, db_session: AsyncSession
    ) -> UpdateEmployeeUsecase:
        empl_gateway = SQLEmployeeGateway(db_session)
        kpi_gateway = SQLKPIGateway(db_session)
        return UpdateEmployeeUsecase(empl_gateway, kpi_gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def create_event_usecase(
        self, db_session: AsyncSession
    ) -> CreateEventUseCase:
        event_gateway = SQLEventGateway(db_session)
        return CreateEventUseCase(event_gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def get_current_events_usecase(
        self, db_session: AsyncSession
    ) -> GetCurrentEventsUseCase:
        event_gateway = SQLEventGateway(db_session)
        return GetCurrentEventsUseCase(event_gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def delete_event_usecase(
        self, db_session: AsyncSession
    ) -> DeleteEventUsecase:
        event_gateway = SQLEventGateway(db_session)
        return DeleteEventUsecase(event_gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def get_events_history_usecase(
        self, db_session: AsyncSession
    ) -> GetEventsHistoryUseCase:
        event_gateway = SQLEventGateway(db_session)
        return GetEventsHistoryUseCase(event_gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def get_kpi_history_usecase(
        self, db_session: AsyncSession
    ) -> GetEmployeesKPIListUseCase:
        kpi_gateway = SQLKPIGateway(db_session)
        return GetEmployeesKPIListUseCase(kpi_gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def get_count_by_department_usecase(
        self, db_session: AsyncSession
    ) -> GetCountByDepartmentUseCase:
        stats_gateway = SQLStatsGateway(db_session)
        return GetCountByDepartmentUseCase(stats_gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def get_company_stats_usecase(
        self, db_session: AsyncSession
    ) -> GetCompanyStatsUsecase:
        stats_gateway = SQLStatsGateway(db_session)
        return GetCompanyStatsUsecase(stats_gateway, db_session)

    @provide(scope=Scope.REQUEST)
    async def get_employee_stats_usecase(
        self, db_session: AsyncSession
    ) -> GetEmployeeStatsUseCase:
        stats_gateway = SQLStatsGateway(db_session)
        return GetEmployeeStatsUseCase(stats_gateway, db_session)

container = make_async_container(AppProvider())
