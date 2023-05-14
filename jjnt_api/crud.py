from typing import Any, Sequence

from sqlalchemy import Result, select, text
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from jjnt_api import models

DECIMAL_NUMBERS = 2

QUERY_DATA_YEAR = """
SELECT c.id_alp2, c.id_alp3, c.name, year, value
FROM {source_id}.{indicator_id}
JOIN countries AS c ON country_id_alp3 = c.id_alp3
WHERE
    year = {year} AND
    country_id_alp3 IN (
        SELECT id_alp3
        FROM countries
        JOIN groups_countries AS gc
        ON countries.id_alp2 = gc.country_id_alp2
        WHERE group_id = '{group_id}'
    )
ORDER BY value DESC;
"""

QUERY_DATA_YEAR_LATEST = """
SELECT c.id_alp2, c.id_alp3, c.name, MAX(i.year) AS year, (
    SELECT value FROM {source_id}.{indicator_id} WHERE country_id_alp3=c.id_alp3 AND year=MAX(i.year)
) AS value
FROM {source_id}.{indicator_id} AS i
JOIN countries AS c ON country_id_alp3 = c.id_alp3
WHERE country_id_alp3 IN (
    SELECT id_alp3
    FROM countries
    JOIN groups_countries AS gc
    ON countries.id_alp2 = gc.country_id_alp2
    WHERE group_id = '{group_id}'
)
GROUP BY c.id_alp2, c.id_alp3, c.name
ORDER BY value DESC;
"""

QUERY_DATA_PERIOD = """
SELECT c.id_alp2, c.id_alp3, c.name, year, value
FROM {source_id}.{indicator_id}
JOIN countries AS c ON country_id_alp3 = c.id_alp3
WHERE
    year >= {year_from} AND
    year <= {year_to} AND
    country_id_alp3 IN (
        SELECT id_alp3
        FROM countries
        JOIN groups_countries AS gc
        ON countries.id_alp2 = gc.country_id_alp2
        WHERE group_id = '{group_id}'
    )
ORDER BY value DESC;
"""

QUERY_DATA_PERIOD_LATEST = """
SELECT c.id_alp2, c.id_alp3, c.name, year, value
FROM {source_id}.{indicator_id}
JOIN countries AS c ON country_id_alp3 = c.id_alp3
WHERE
    year >= {year_from} AND
    country_id_alp3 IN (
        SELECT id_alp3
        FROM countries
        JOIN groups_countries AS gc
        ON countries.id_alp2 = gc.country_id_alp2
        WHERE group_id = '{group_id}'
    )
ORDER BY value DESC;
"""


async def read_indicators(session: AsyncSession) -> Sequence[models.Indicator]:
    result_set: Result[Any] = await session.execute(select(models.Indicator).order_by(models.Indicator.id))
    return result_set.scalars().all()


async def read_categories(session: AsyncSession) -> Sequence[models.Category]:
    result_set: Result[Any] = await session.execute(
        select(models.Category).options(selectinload(models.Category.indicators)).order_by(models.Category.id),
    )
    return result_set.scalars().all()


async def read_indicator_detail(source_id: str, indicator_id: str, session: AsyncSession) -> dict:
    query = f"""
    SELECT
        i.id           AS i_id,
        i.abbreviation AS i_abbreviation,
        i.name         AS i_name,
        i.description  AS i_description,
        i.unit         AS i_unit,
        i.asc_ordering AS i_asc_ordering,
        s.id           AS default_source_id
    FROM sources_indicators AS si
        JOIN indicators AS i ON si.indicator_id = i.id
        JOIN sources AS s ON si.source_id = s.id
    WHERE
        si.indicator_id = '{indicator_id}' AND
        si.source_id = '{source_id}';
    """

    result_set: Result[Any] = await session.execute(text(query))
    row: Row[Any] | None = result_set.first()

    return (
        {
            "id": row[0],
            "abbreviation": row[1],
            "name": row[2],
            "description": row[3],
            "unit": row[4],
            "ascOrdering": row[5],
            "defaultSourceId": row[6],
        }
        if row
        else {}
    )


async def read_source_detail(source_id: str, indicator_id: str, session: AsyncSession) -> dict:
    query = f"""
    SELECT s.id       AS source_id,
        s.name        AS source_name,
        s.description AS source_description,
        s.url         AS source_url,
        si.url_src    AS source_indicator_url
    FROM sources AS s
        JOIN sources_indicators AS si ON s.id = si.source_id
    WHERE
        si.indicator_id = '{indicator_id}' AND
        si.source_id = '{source_id}';
    """

    result_set: Result[Any] = await session.execute(text(query))
    row: Row[Any] | None = result_set.first()

    return (
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "url": row[3],
            "indicatorUrl": row[4],
        }
        if row
        else {}
    )


async def read_options_charts(session: AsyncSession) -> list[dict]:
    query = "SELECT id, name FROM charts;"

    result_set: Result[Any] = await session.execute(text(query))
    row: Sequence[Row[Any]] = result_set.fetchall()

    return (
        [
            {
                "id": elem[0],
                "label": elem[1],
            }
            for elem in row
        ]
        if row
        else []
    )


async def read_options_groups(session: AsyncSession) -> list[dict]:
    query = "SELECT id, name FROM groups;"

    result_set: Result[Any] = await session.execute(text(query))
    row: Sequence[Row[Any]] = result_set.fetchall()

    return (
        [
            {
                "id": elem[0],
                "label": elem[1],
            }
            for elem in row
        ]
        if row
        else []
    )


async def read_options_sources(indicator_id: str, session: AsyncSession) -> list[dict]:
    query = f"""
    SELECT s.id, s.name
    FROM sources_indicators AS si
    JOIN sources AS s ON si.source_id = s.id
    WHERE indicator_id = '{indicator_id}'
    ORDER BY s.id;
    """

    result_set: Result[Any] = await session.execute(text(query))
    row: Sequence[Row[Any]] = result_set.fetchall()

    return (
        [
            {
                "id": elem[0],
                "label": elem[1],
            }
            for elem in row
        ]
        if row
        else []
    )


async def read_options_years(source_id: str, indicator_id: str, group_id: str, session: AsyncSession) -> list[dict]:
    query = f"""
    SELECT DISTINCT year
    FROM {source_id}.{indicator_id}
    JOIN countries AS c ON country_id_alp3 = c.id_alp3
    WHERE
        country_id_alp3 IN (
            SELECT id_alp3
            FROM countries
            JOIN groups_countries AS gc
            ON countries.id_alp2 = gc.country_id_alp2
            WHERE group_id = '{group_id}'
        )
    ORDER BY year;
    """

    result_set: Result[Any] = await session.execute(text(query))
    row: Sequence[Row[Any]] = result_set.fetchall()
    row_ = [elem._asdict() if isinstance(elem, Row) else elem for elem in row]  # noqa: WPS437

    return [
        {
            "id": elem["year"],
            "label": elem["year"],
        }
        for elem in row_
    ] + [
        {
            "id": "posledni_znamy",
            "label": "Poslední známý",
        },
    ]


async def read_data_table(
    source_id: str,
    indicator_id: str,
    group_id: str,
    year: int | None,
    session: AsyncSession,
) -> list[dict]:
    query = (
        QUERY_DATA_YEAR_LATEST.format(
            source_id=source_id,
            indicator_id=indicator_id,
            group_id=group_id,
        )
        if year is None
        else QUERY_DATA_YEAR.format(
            source_id=source_id,
            indicator_id=indicator_id,
            group_id=group_id,
            year=year,
        )
    )

    result_set: Result[Any] = await session.execute(text(query))
    row: Sequence[Row[Any]] = result_set.fetchall()

    return (
        [
            {
                "id": i + 1,
                "country": {
                    "idAlp2": elem[0],
                    "idAlp3": elem[1],
                    "name": elem[2],
                },
                "year": elem[3],
                "value": round(elem[4], DECIMAL_NUMBERS),
            }
            for i, elem in enumerate(row)
        ]
        if row
        else []
    )


async def read_data_map(
    source_id: str,
    indicator_id: str,
    group_id: str,
    year: int | None,
    session: AsyncSession,
) -> list[list]:
    query = (
        QUERY_DATA_YEAR_LATEST.format(
            source_id=source_id,
            indicator_id=indicator_id,
            group_id=group_id,
        )
        if year is None
        else QUERY_DATA_YEAR.format(
            source_id=source_id,
            indicator_id=indicator_id,
            group_id=group_id,
            year=year,
        )
    )

    result_set: Result[Any] = await session.execute(text(query))
    row: Sequence[Row[Any]] = result_set.fetchall()

    result = [["countryIdAlp2", "countryName", "Hodnota", "Rok"]]

    for elem in row:
        result.append([str(elem[0]), str(elem[2]), round(elem[4], DECIMAL_NUMBERS), elem[3]])

    return result


async def read_data_barpiechart(
    source_id: str,
    indicator_id: str,
    group_id: str,
    year: int | None,
    session: AsyncSession,
) -> list[list]:
    query = (
        QUERY_DATA_YEAR_LATEST.format(
            source_id=source_id,
            indicator_id=indicator_id,
            group_id=group_id,
        )
        if year is None
        else QUERY_DATA_YEAR.format(
            source_id=source_id,
            indicator_id=indicator_id,
            group_id=group_id,
            year=year,
        )
    )

    result_set: Result[Any] = await session.execute(text(query))
    row: Sequence[Row[Any]] = result_set.fetchall()

    result = [["Země", "Hodnota"]] if year is None else [["Země", f"Hodnota, {year}"]]

    for elem in row:
        result.append([elem[2], elem[4]])

    return result


async def read_data_linechart(
    source_id: str,
    indicator_id: str,
    group_id: str,
    year_from: int,
    year_to: int | None,
    session: AsyncSession,
) -> list[list]:
    query = (
        QUERY_DATA_PERIOD_LATEST.format(
            source_id=source_id,
            indicator_id=indicator_id,
            group_id=group_id,
            year_from=year_from,
        )
        if year_to is None
        else QUERY_DATA_PERIOD.format(
            source_id=source_id,
            indicator_id=indicator_id,
            group_id=group_id,
            year_from=year_from,
            year_to=year_to,
        )
    )

    result_set: Result[Any] = await session.execute(text(query))
    data: Sequence[Row[Any]] = result_set.fetchall()

    countries = list({elem[2] for elem in data})
    years = list({elem[3] for elem in data})
    years.sort()

    result = [["Rok"] + countries]

    for year in years:
        row = [year]
        for country in countries:
            try:
                value = next(filter(lambda a: a[2] == country and a[3] == year, data))[4]
            except StopIteration:
                value = None
            row.append(value)
        result.append(row)

    return result
