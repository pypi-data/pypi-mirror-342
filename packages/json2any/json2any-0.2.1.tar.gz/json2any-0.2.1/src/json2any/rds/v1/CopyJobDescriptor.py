from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CopyJobDescriptor:
    name: str
    src: str = field(metadata=dict(description='Name of the template file'))
    dst: str = field(default_factory=Path)
    output_override: bool = field(default=True)
    enabled: bool = field(default=True)
