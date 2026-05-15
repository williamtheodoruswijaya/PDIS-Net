from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Location:
    latitude: Optional[float]
    longitude: Optional[float]
    altitude_m: Optional[float] = None
    source: str = "none"


class TelemetryProvider:
    def __init__(
        self,
        manual_latitude: Optional[float] = None,
        manual_longitude: Optional[float] = None,
        telemetry_file: Optional[Path] = None,
    ) -> None:
        self.manual_latitude = manual_latitude
        self.manual_longitude = manual_longitude
        self.telemetry_file = telemetry_file

    def read(self) -> Location:
        file_location = self._read_file()
        if file_location is not None:
            return file_location

        if self.manual_latitude is not None or self.manual_longitude is not None:
            return Location(
                latitude=self.manual_latitude,
                longitude=self.manual_longitude,
                source="manual",
            )

        return Location(latitude=None, longitude=None)

    def _read_file(self) -> Optional[Location]:
        if self.telemetry_file is None or not self.telemetry_file.exists():
            return None

        try:
            payload = json.loads(self.telemetry_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

        latitude = payload.get("latitude", payload.get("lat"))
        longitude = payload.get("longitude", payload.get("lon", payload.get("lng")))
        altitude = payload.get("altitude_m", payload.get("alt"))

        return Location(
            latitude=_to_float(latitude),
            longitude=_to_float(longitude),
            altitude_m=_to_float(altitude),
            source=str(payload.get("source", "telemetry-file")),
        )


def _to_float(value) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

