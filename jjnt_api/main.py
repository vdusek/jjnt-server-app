from typing import Any, Literal, Sequence

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from jjnt_api import crud, models, schemas
from jjnt_api.consts import LATEST_KNOWN
from jjnt_api.database import get_async_session
from jjnt_api.log_config import logger
from jjnt_api.responses import PrettyJsonResponse

# FastAPI app
app = FastAPI()

# Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "https://jakjsmenatom.cz",
        "https://www.jakjsmenatom.cz",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> PrettyJsonResponse:
    logger.debug("Log message from root endpoint")
    content = {"message": "Swagger documentation is available on /docs endpoint."}
    return PrettyJsonResponse(content, indent=2)


@app.get(
    path="/indicators/",
    response_model=list[schemas.Indicator],
)
async def get_indicators(
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> Sequence[models.Indicator]:
    """
    Get a list of the all indicators.
    """
    logger.debug("Log message from get_indicators endpoint")
    return await crud.read_indicators(session)


@app.get(
    path="/categories/",
    response_model=list[schemas.Category],
)
async def get_categories(
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> Sequence[models.Category]:
    """
    Get a list of the all categories and their indicators.
    """
    logger.debug("Log message from get_categories endpoint")
    return await crud.read_categories(session)


@app.get(
    path="/indicators/{source_id}/{indicator_id}/",
    response_model=schemas.IndicatorDetail,
)
async def get_indicator_detail(
    source_id: str,
    indicator_id: str,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> dict:
    """
    Get indicator detail.
    """
    logger.debug("Log message from get_indicator_detail endpoint")
    indicator = await crud.read_indicator_detail(source_id, indicator_id, session)
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return indicator


@app.get(
    path="/sources/{source_id}/{indicator_id}",
    response_model=schemas.SourceDetail,
)
async def get_source_detail(
    source_id: str,
    indicator_id: str,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> dict:
    """
    Get source detail.
    """
    logger.debug("Log message from get_source_detail endpoint")
    source = await crud.read_source_detail(source_id, indicator_id, session)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@app.get(
    path="/options/charts/",
    response_model=list[schemas.Option],
)
async def get_options_charts(
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> list[dict]:
    """
    Get a list of the all charts.
    """
    logger.debug("Log message from get_options_charts endpoint")
    return await crud.read_options_charts(session)


@app.get(
    path="/options/groups/",
    response_model=list[schemas.Option],
)
async def get_options_groups(
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> list[dict]:
    """
    Get a list of the all groups of countries.
    """
    logger.debug("Log message from get_options_groups endpoint")
    return await crud.read_options_groups(session)


@app.get(
    path="/options/sources/{indicator_id}/",
    response_model=list[schemas.Option],
)
async def get_options_sources(
    indicator_id: str,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> list[dict]:
    """
    Get a list of the all sources for a specific indicator.
    """
    logger.debug("Log message from get_options_sources endpoint")
    return await crud.read_options_sources(indicator_id, session)


@app.get(
    path="/options/years/{source_id}/{indicator_id}/{group_id}/",
    response_model=list[schemas.Option],
)
async def get_options_years(
    source_id: str,
    indicator_id: str,
    group_id: str,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> list[dict]:
    """
    Get a list of the years for a specific source, indicator and group.
    """
    logger.debug("Log message from get_options_years endpoint")
    return await crud.read_options_years(source_id, indicator_id, group_id, session)


@app.get(
    path="/data/tabulka/{source_id}/{indicator_id}/{group_id}/{year}/",
    response_model=list[schemas.DataTable],
)
async def get_data_table(
    source_id: str,
    indicator_id: str,
    group_id: str,
    year: int | Literal["posledni_znamy"],
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> list[dict]:
    """
    Get data for a table chart for a specific source, indicator, group and year.
    """
    logger.debug("Log message from get_data_table endpoint")
    year_ = None if year == LATEST_KNOWN else year
    return await crud.read_data_table(source_id, indicator_id, group_id, year_, session)  # type: ignore


@app.get(
    path="/data/mapa/{source_id}/{indicator_id}/{group_id}/{year}/",
    response_model=list[list[Any]],
)
async def get_data_map(
    source_id: str,
    indicator_id: str,
    group_id: str,
    year: int | Literal["posledni_znamy"],
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> list[list]:
    """
    Get data for a map chart for a specific source, indicator, group and year.
    """
    logger.debug("Log message from get_data_map endpoint")
    year_ = None if year == LATEST_KNOWN else year
    return await crud.read_data_map(source_id, indicator_id, group_id, year_, session)  # type: ignore


@app.get(
    path="/data/sloupcovy_graf/{source_id}/{indicator_id}/{group_id}/{year}/",
    response_model=list[list[Any]],
)
async def get_data_barchart(
    source_id: str,
    indicator_id: str,
    group_id: str,
    year: int | Literal["posledni_znamy"],
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> list[list]:
    """
    Get data for a bar chart for a specific source, indicator, group and year.
    """
    logger.debug("Log message from get_data_barchart endpoint")
    year_ = None if year == LATEST_KNOWN else year
    return await crud.read_data_barpiechart(source_id, indicator_id, group_id, year_, session)  # type: ignore


@app.get(
    path="/data/kolacovy_graf/{source_id}/{indicator_id}/{group_id}/{year}/",
    response_model=list[list[Any]],
)
async def get_data_piechart(
    source_id: str,
    indicator_id: str,
    group_id: str,
    year: int | Literal["posledni_znamy"],
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> list[list]:
    """
    Get data for a pie chart for a specific source, indicator, group and year.
    """
    logger.debug("Log message from get_data_piechart endpoint")
    year_ = None if year == LATEST_KNOWN else year
    return await crud.read_data_barpiechart(source_id, indicator_id, group_id, year_, session)  # type: ignore


@app.get(
    path="/data/liniovy_graf/{source_id}/{indicator_id}/{group_id}/{year_from}/{year_to}/",
    response_model=list[list[Any]],
)
async def get_data_linechart(
    source_id: str,
    indicator_id: str,
    group_id: str,
    year_from: int | Literal["posledni_znamy"],
    year_to: int | Literal["posledni_znamy"],
    session: AsyncSession = Depends(get_async_session),  # noqa: B008, WPS404
) -> list[list]:
    """
    Get data for a line chart for a specific source, indicator, group, year from and year to.
    """
    logger.debug("Log message from get_data_linechart endpoint")
    year_to_ = None if year_to == LATEST_KNOWN else year_to
    return await crud.read_data_linechart(source_id, indicator_id, group_id, year_from, year_to_, session)  # type: ignore # noqa: E501
