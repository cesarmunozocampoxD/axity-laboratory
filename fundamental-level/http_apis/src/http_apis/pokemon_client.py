"""
Lab practice: httpx client with retries, timeouts, and streaming download.
"""

import logging
import time
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_URL = "https://pokeapi.co/api/v2"

# Fine-grained timeout: each phase has its own limit (seconds)
TIMEOUT = httpx.Timeout(connect=5.0, read=15.0, write=5.0, pool=5.0)

MAX_RETRIES = 3
BACKOFF_BASE = 1.0  # seconds; grows as 1 → 2 → 4 …
CHUNK_SIZE = 8_192  # 8 KB per chunk for streaming downloads

# HTTP status codes that are worth retrying (server-side / rate-limit issues)
RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 500, 502, 503, 504})

# Network-level exceptions that are also worth retrying
RETRYABLE_EXCEPTIONS = (
    httpx.TimeoutException,
    httpx.ConnectError,
    httpx.RemoteProtocolError,
)


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class PokemonClient:
    """
    httpx-based client for the PokeAPI (https://pokeapi.co/).
    """

    def __init__(
        self,
        max_retries: int = MAX_RETRIES,
        backoff_base: float = BACKOFF_BASE,
    ) -> None:
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self._client = httpx.Client(
            base_url=BASE_URL,
            timeout=TIMEOUT,
            headers={"Accept": "application/json"},
            follow_redirects=True,
        )

    def __enter__(self) -> "PokemonClient":
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def _get_with_retry(self, path: str, **kwargs: object) -> httpx.Response:
        """
        Perform GET *path* with automatic retry + exponential backoff.
        """
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self._client.get(path, **kwargs)

                if response.status_code not in RETRYABLE_STATUS_CODES:
                    return response

                logger.warning(
                    "Attempt %d/%d — HTTP %d for %s",
                    attempt,
                    self.max_retries,
                    response.status_code,
                    path,
                )
                last_error = httpx.HTTPStatusError(
                    message=f"HTTP {response.status_code}",
                    request=response.request,
                    response=response,
                )

            except RETRYABLE_EXCEPTIONS as exc:
                logger.warning(
                    "Attempt %d/%d — %s: %s",
                    attempt,
                    self.max_retries,
                    type(exc).__name__,
                    exc,
                )
                last_error = exc

            if attempt < self.max_retries:
                delay = self.backoff_base * (2 ** (attempt - 1))
                logger.info("Waiting %.1f s before next attempt…", delay)
                time.sleep(delay)

        raise RuntimeError(
            f"All {self.max_retries} attempts failed for {path}"
        ) from last_error

    # ------------------------------------------------------------------
    # Public API — data endpoints
    # ------------------------------------------------------------------

    def get_pokemon(self, name_or_id: str | int) -> dict:
        """
        Fetch a Pokemon by name (e.g. ``'pikachu'``) or Pokédex ID (e.g. ``25``).
        Returns the full JSON payload as a Python dict.
        """

        response = self._get_with_retry(f"/pokemon/{name_or_id}")
        response.raise_for_status()
        return response.json()

    def get_pokemon_list(self, limit: int = 20, offset: int = 0) -> dict:
        """
        Fetch a paginated list of Pokemon.

        Parameters
        ----------
        limit:  Maximum number of results (default 20).
        offset: Starting position in the full list (default 0).
        """
        response = self._get_with_retry(
            "/pokemon", params={"limit": limit, "offset": offset}
        )
        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Public API — streaming download
    # ------------------------------------------------------------------

    def download_sprite(
        self,
        sprite_url: str,
        destination: Path | str,
        chunk_size: int = CHUNK_SIZE,
    ) -> Path:
        """
        Stream-download a Pokemon sprite and save it to *destination*.
        """
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Streaming sprite  %s  →  %s", sprite_url, destination)

        with httpx.stream(
            "GET", sprite_url, timeout=TIMEOUT, follow_redirects=True
        ) as response:
            response.raise_for_status()

            bytes_written = 0
            with open(destination, "wb") as file:
                for chunk in response.iter_bytes(chunk_size=chunk_size):
                    file.write(chunk)
                    bytes_written += len(chunk)

        logger.info("Saved  %s  (%.1f KB)", destination.name, bytes_written / 1024)
        return destination
