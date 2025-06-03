# main.py
"""Che Ore Sono API v1.1.0

Questo micro‑servizio FastAPI espone un solo endpoint (`/che_ore_sono`) che
restituisce la data e l'ora correnti nel fuso orario **Europe/Rome** in formato
`YYYY-MM-DD HH:MM:SS`.

È stato aggiunto un controllo esplicito sui dati IANA per evitare l'errore
`ZoneInfoNotFoundError` che può verificarsi su Windows quando non è installato
il pacchetto `tzdata`.
"""

from __future__ import annotations

from datetime import datetime
from typing import Final

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

try:
    # Python ≥ 3.9
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover — Python < 3.9
    # Fallback per Python 3.8 o inferiore
    from backports.zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # type: ignore

TZ_NAME: Final[str] = "Europe/Rome"


def get_rome_tz() -> ZoneInfo:
    """Restituisce l'oggetto :class:`ZoneInfo` per *Europe/Rome*.

    Se i dati IANA non sono presenti (tipico su Windows senza *tzdata*),
    viene sollevata una :class:`fastapi.HTTPException` con dettagli su come
    risolvere il problema.
    """

    try:
        return ZoneInfo(TZ_NAME)
    except ZoneInfoNotFoundError as exc:  # pragma: no cover
        raise HTTPException(
            status_code=500,
            detail=(
                f"Timezone data for '{TZ_NAME}' not found: {exc}. "
                "Install the 'tzdata' package (e.g. `pip install tzdata`) or "
                "ensure the OS provides the IANA time‑zone database."
            ),
        )


app = FastAPI(
    title="Che Ore Sono API",
    version="1.1.0",
    summary="API che restituisce data e ora correnti nel fuso orario Europe/Rome.",
)


@app.get(
    "/che_ore_sono",
    response_class=PlainTextResponse,
    summary="Data e ora correnti (Europe/Rome)",
)
async def che_ore_sono() -> str:
    """Endpoint principale: ritorna **YYYY-MM-DD HH:MM:SS** timezone Europe/Rome."""

    now = datetime.now(get_rome_tz())
    return now.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8111, reload=True)
