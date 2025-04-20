from dataclasses import dataclass, field
from typing import List, Optional

from json2any.rds.v3.JobDescriptor import JobDescriptor


@dataclass
class Json2AnyDescriptor:
    name: str = field(metadata=dict(description="Name of the Generator run - for debugging purposes"))

    data_schema_id: Optional[str] = field(default=None,
                                          metadata=dict(description="Optional data schema to use for validation"))

    template_provider: Optional[str] = field(default=None,
                                             metadata=dict(description='Template Provider to use'))

    template_location: Optional[str] = field(default=None, metadata=dict(
        description='Location of templates - format depends on Template Provider used'))

    jobs: List[JobDescriptor] = field(default_factory=list,
                                      metadata=dict(description='Job descriptors'))
