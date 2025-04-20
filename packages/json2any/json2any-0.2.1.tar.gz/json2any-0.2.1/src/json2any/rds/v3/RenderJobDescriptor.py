from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class RenderJobDescriptor:
    name: str
    templates_path: Optional[str] = field(metadata=dict(
        description='Optional path to templates. This is relative to "Json2AnyDescriptor.template_location"'))
    template: str = field(metadata=dict(description='Name of the Jinja2 template file'))

    query: Optional[str] = field(metadata=dict(description='JSONPath Next-Generation query to run on data loaded'))
    query_for_each: bool = field(default=False, metadata=dict(
        description='If set to true the result of the query is expected to be a list and template is rendered for each item in list.'
                    'Otherwise the output of the query  is rendered once using template'))

    output_file_pattern: Optional[str] = field(default=None, metadata=dict(
        description='Optional output file pattern as Jinja2 template'))
    output_override: bool = field(default=True, metadata=dict(
        description='Automatically override output file if set, Otherwise error will be thrown if file already exists'))
    run_data: Any = field(default=None, metadata=dict(
        description='Arbitrary data to pass to Jinja2 template. The data will be mounted under "run_data" key'))
    enabled: bool = field(default=True, metadata=dict(description='Whatever the Job is enabled'))
