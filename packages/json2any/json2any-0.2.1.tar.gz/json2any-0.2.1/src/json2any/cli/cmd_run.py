from argparse import Namespace
from logging import getLogger
from pathlib import Path

from json2any.JinjaExecutor import JinjaExecutor
from json2any.ProviderPlugins import ProviderPlugins
from json2any.rds import Json2AnyDescriptor
from json2any.rds.schema_utils import load_data_w_schema

plugins = ProviderPlugins()
plugins.find_plugins()

log = getLogger(__name__)


def cmd_run_setup(subparsers):
    global plugins

    parser = subparsers.add_parser('run', help='Generate the output according to RDS')

    parser.add_argument('rds_file', type=Path, help='Path to runs descriptor file')
    parser.add_argument('-o', '--out-dir', type=Path, help='Path to output directory', default=Path.cwd())

    plugins.update_arg_parser(parser)

    parser.set_defaults(func=cmd_run_execute)


def cmd_run_execute(args: Namespace):
    global plugins

    plugins.process_args(args)

    rds_file: Path = args.rds_file
    rds_file = rds_file.resolve().absolute()

    log.debug('Loading Runs Descriptor from "%s"', rds_file)

    rds = load_data_w_schema(rds_file, Json2AnyDescriptor)

    template_provider = plugins.get_template_provider(str(rds_file.parent), rds)

    out_dir: Path = args.out_dir
    out_dir = out_dir.resolve().absolute()
    if not out_dir.is_dir():
        log.trace('Output Folder does not exists - creating: %s', out_dir)
        out_dir.mkdir(parents=True)
    log.debug('Output will be written to: "%s"', out_dir)

    data = plugins.load_data()

    executor = JinjaExecutor(template_provider, plugins.active_help_providers, rds, data, out_dir=out_dir)

    executor.execute_runs()
