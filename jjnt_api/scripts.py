import uvicorn


def run_dev() -> None:
    """
    Launched with `poetry run dev` at root level.
    """
    uvicorn.run("jjnt_api.main:app", host="127.0.0.1", port=8000, reload=True)
