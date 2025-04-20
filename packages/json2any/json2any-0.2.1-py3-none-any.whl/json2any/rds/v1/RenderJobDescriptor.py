from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class RenderJobDescriptor:
    name: str
    template: str = field(metadata=dict(description='Name of the template file'))

    query: Optional[str] = field(metadata=dict(description='Name of the template file'))
    query_for_each: bool = field(default=False)

    output_file_pattern: Optional[str] = field(default=None)
    output_override: bool = field(default=True)
    run_data: Any = field(default=None)
    enabled: bool = field(default=True)
