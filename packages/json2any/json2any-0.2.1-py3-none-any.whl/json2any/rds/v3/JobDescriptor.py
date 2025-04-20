from dataclasses import dataclass, field
from typing import Optional

from json2any.Json2AnyException import Json2AnyException
from json2any.rds.v3.CopyJobDescriptor import CopyJobDescriptor
from json2any.rds.v3.RenderJobDescriptor import RenderJobDescriptor


@dataclass
class JobDescriptor:
    copy_job: Optional[CopyJobDescriptor] = field(
        metadata=dict(description='Copy job descriptor. If set then the "render_job" should not be populated.'))
    render_job: Optional[RenderJobDescriptor] = field(
        metadata=dict(description='Rendering job descriptor. If set then the "copy_job" should not be populated.'))

    def __post_init__(self):
        if self.copy_job and self.render_job:
            raise Json2AnyException('Either "copy_job" or "render_job" must be specified NOT both')

    @property
    def enabled(self) -> bool:
        if self.copy_job:
            return self.copy_job.enabled
        elif self.render_job:
            return self.render_job.enabled
        else:
            return False

    @property
    def name(self) -> str:
        if self.copy_job:
            return self.copy_job.name
        elif self.render_job:
            return self.render_job.name
        else:
            return ''
