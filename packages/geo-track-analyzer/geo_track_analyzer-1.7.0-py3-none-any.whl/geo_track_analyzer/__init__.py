"""Analyze geospacial data tracks"""

from .cli import extract_track, update_elevation
from .enhancer import (
    ElevationEnhancer,
    Enhancer,
    EnhancerType,
    OpenElevationEnhancer,
    OpenTopoElevationEnhancer,
    get_enhancer,
)
from .track import ByteTrack, FITTrack, GPXFileTrack, PyTrack, SegmentTrack, Track

__all__ = [
    "ByteTrack",
    "ElevationEnhancer",
    "Enhancer",
    "EnhancerType",
    "FITTrack",
    "GPXFileTrack",
    "OpenElevationEnhancer",
    "OpenTopoElevationEnhancer",
    "PyTrack",
    "SegmentTrack",
    "Track",
    "extract_track",
    "get_enhancer",
    "update_elevation",
]

__version__ = "1.6.3"
