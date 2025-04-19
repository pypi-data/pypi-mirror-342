ENRICH_UNITS: dict[str, str] = {
    "elevation": "m",
    "speed": "km/h",
    "heartrate": "bpm",
    "cadence": "rpm",
    "power": "W",
    "distance": "km",
    "temperature": "°C",
}

# Based on plotly.express.colors.sequential.Plotly3
DEFAULT_COLOR_GRADIENT: tuple[str, str] = ("#0508b8", "#fec3fe")

COLOR_GRADIENTS: dict[str, tuple[str, str]] = {
    "heartrate": ("#636EFA", "#EF553B"),
}

DEFAULT_BAR_COLORS: tuple[str, str] = ("#7570b3", "#8da0cb")
