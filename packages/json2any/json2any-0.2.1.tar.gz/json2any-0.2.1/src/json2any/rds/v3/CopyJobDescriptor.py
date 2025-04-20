from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CopyJobDescriptor:
    name: str
    src: str = field(metadata=dict(description='Source path/file'))
    dst: str = field(default_factory=Path, metadata=dict(description='Destination path/file'))
    output_override: bool = field(default=True, metadata=dict(description='Allow to override output file'))
    enabled: bool = field(default=True, metadata=dict(description='Whatever the Job is enabled'))
