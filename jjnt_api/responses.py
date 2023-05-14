import json
from typing import Any

from fastapi.responses import Response


class PrettyJsonResponse(Response):
    media_type = "application/json"

    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        indent: int | None = None,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
    ) -> None:
        self.indent = indent
        super().__init__(content, status_code, headers, media_type)

    def render(self, content: Any) -> bytes:
        s = json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=self.indent,
            separators=(",", ": "),
        )
        return f"{s}\n".encode("utf-8")
