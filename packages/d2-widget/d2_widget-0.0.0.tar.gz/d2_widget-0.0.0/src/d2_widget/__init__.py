import importlib.metadata
import pathlib

import anywidget
import traitlets
from typing import TypedDict, Optional, Literal, Annotated

try:
    __version__ = importlib.metadata.version("d2-widget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class RenderOptions(TypedDict, total=False):
    """Matches RenderOptions from @terrastruct/d2"""

    sketch: Annotated[
        bool,
        "Enable sketch mode [default: false]",
    ]
    themeID: Annotated[
        int,
        "Theme ID to use [default: 0]",
    ]
    darkThemeID: Annotated[
        int,
        "Theme ID to use when client is in dark mode",
    ]
    center: Annotated[
        bool,
        "Center the SVG in the containing viewbox [default: false]",
    ]
    pad: Annotated[
        int,
        "Pixels padded around the rendered diagram [default: 100]",
    ]
    scale: Annotated[
        float,
        "Scale the output",
    ]
    forceAppendix: Annotated[
        bool,
        "Adds an appendix for tooltips and links [default: false]",
    ]
    target: Annotated[
        str,
        "Target board/s to render",
    ]
    animateInterval: Annotated[
        int,
        "Multiple boards transition interval (in milliseconds)",
    ]
    salt: Annotated[
        str,
        "Add a salt value to ensure the output uses unique IDs",
    ]
    noXMLTag: Annotated[
        bool,
        "Omit XML tag from output SVG files",
    ]


class CompileOptions(RenderOptions, total=False):
    """Matches CompileOptions from @terrastruct/d2"""

    layout: Annotated[
        Literal["dagre", "elk"],
        "Layout engine to use [default: 'dagre']",
    ]
    fontRegular: Annotated[
        bytes,
        "A byte array containing .ttf file for regular font",
    ]
    fontItalic: Annotated[
        bytes,
        "A byte array containing .ttf file for italic font",
    ]
    fontBold: Annotated[
        bytes,
        "A byte array containing .ttf file for bold font",
    ]
    fontSemibold: Annotated[
        bytes,
        "A byte array containing .ttf file for semibold font",
    ]


class D2Widget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    
    _svg = traitlets.Unicode().tag(sync=True)
    diagram = traitlets.Unicode().tag(sync=True)
    options = traitlets.Dict({}).tag(sync=True)

    def __init__(self, diagram: str, options: Optional[CompileOptions] = None):
        super().__init__()
        self.diagram = diagram
        self.options = options or {}

    @property
    def svg(self) -> str:
        return self._svg
