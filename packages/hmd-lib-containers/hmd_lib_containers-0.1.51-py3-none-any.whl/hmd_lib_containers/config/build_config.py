from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Union


@dataclass
class ImageBuildSecret:
    id: str
    src: str = None


@dataclass
class ImageBuildConfig:
    context_dir: Union[str, Path] = Path("./")
    build_args: Dict[str, Any] = field(default_factory=lambda: {})
    cache: bool = False
    dockerfile: Union[str, Path] = Path("./src/docker/Dockerfile")
    secrets: List[ImageBuildSecret] = field(default_factory=lambda: [])
    platforms: List[str] = field(default_factory=lambda: ["linux/amd64", "linux/arm64"])
    network: str = None
    progress: str = "plain"
    install_local: bool = False
