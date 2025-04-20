from dataclasses import dataclass, field
from typing import Optional, List

from json2any.rds.v1.JobDescriptor import JobDescriptor


@dataclass
class Json2AnyDescriptor:
    name: str = field(metadata=dict(description="Name of the Generator run - for debugging purposes"))

    template_location: Optional[str] = field(default=None, metadata=dict(
        description='Location of templates - format depends on Template Provider used'))

    template_provider: Optional[str] = field(default='FileSystem',
                                             metadata=dict(description='Template Provider to use'))

    jobs: List[JobDescriptor] = field(default_factory=list,
                                      metadata=dict(description='Job descriptors'))
