from dataclasses import dataclass, field
from typing import Optional

from json2any.rds.v1.CopyJobDescriptor import CopyJobDescriptor
from json2any.rds.v1.RenderJobDescriptor import RenderJobDescriptor


@dataclass
class JobDescriptor:
    copy_job: Optional[CopyJobDescriptor] = field(metadata=dict(description='Copy job'))
    render_job: Optional[RenderJobDescriptor] = field(metadata=dict(description='Rendering job'))

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
