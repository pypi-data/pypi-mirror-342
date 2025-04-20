from argparse import ArgumentParser

from jinja2.loaders import PackageLoader, FileSystemLoader

from json2any.ProviderPlugins import ProviderPlugins
from json2any.cli_logg_utils import cli_logg_util_setup, cli_logg_util_setup_parser
from json2any.providers.template.FileSystemTemplateProvider import FileSystemTemplateProvider
from json2any.providers.template.PackageTemplateProvider import PackageTemplateProvider
from json2any.rds.v3.Json2AnyDescriptor import Json2AnyDescriptor

ARGS_PACKAGE_PATH = 'schema'
RDS_PACKAGE_PATH = ''

ARGS_PACKAGE_NAME = 'json2any'
RDS_PACKAGE_NAME = 'json2any_plugin'


def test_get_template_provider_default():
    pp = ProviderPlugins()
    fstp = FileSystemTemplateProvider()
    ptp = PackageTemplateProvider()
    pp.providers.append(fstp)
    pp.providers.append(ptp)
    parser = ArgumentParser()
    cli_logg_util_setup_parser(parser)

    pp.update_arg_parser(parser)

    args = parser.parse_args({})
    cli_logg_util_setup(args)
    pp.process_args(args)

    assert len(pp.active_providers) == 0
    rds = Json2AnyDescriptor('test_rds', template_location=RDS_PACKAGE_NAME)
    tp = pp.get_template_provider('path', rds)
    assert tp == fstp

    fsl: FileSystemLoader = fstp.get_loader(RDS_PACKAGE_PATH)
    assert RDS_PACKAGE_NAME in fsl.searchpath


def test_get_template_provider_args():
    pp = ProviderPlugins()
    fstp = FileSystemTemplateProvider()
    ptp = PackageTemplateProvider()
    pp.providers.append(fstp)
    pp.providers.append(ptp)

    parser = ArgumentParser()
    cli_logg_util_setup_parser(parser)

    pp.update_arg_parser(parser)

    args = parser.parse_args(args=[
        '--ptp-package',
        ARGS_PACKAGE_NAME,
        '--ptp-path',
        ARGS_PACKAGE_PATH
    ]
    )
    cli_logg_util_setup(args)
    pp.process_args(args)

    assert len(pp.active_providers) == 1
    rds = Json2AnyDescriptor(name='test_rds', template_location=RDS_PACKAGE_NAME)
    tp: PackageTemplateProvider = pp.get_template_provider('rds_path', rds)
    assert tp == ptp

    ldr: PackageLoader = tp.get_loader(RDS_PACKAGE_PATH)
    assert tp.package_name == ARGS_PACKAGE_NAME
    assert tp.package_path == ARGS_PACKAGE_PATH

    assert ldr.package_name == ARGS_PACKAGE_NAME
    assert ldr.package_path == ARGS_PACKAGE_PATH


def test_get_template_provider_args_mixed():
    pp = ProviderPlugins()
    fstp = FileSystemTemplateProvider()
    ptp = PackageTemplateProvider()
    pp.providers.append(fstp)
    pp.providers.append(ptp)

    parser = ArgumentParser()
    cli_logg_util_setup_parser(parser)

    pp.update_arg_parser(parser)

    args = parser.parse_args(args=[
        '--ptp-package',
        ARGS_PACKAGE_NAME
    ]
    )
    cli_logg_util_setup(args)
    pp.process_args(args)

    assert len(pp.active_providers) == 1
    rds = Json2AnyDescriptor(name='test_rds', template_location=RDS_PACKAGE_NAME)
    tp: PackageTemplateProvider = pp.get_template_provider('rds_path', rds)
    assert tp == ptp

    ldr: PackageLoader = tp.get_loader(RDS_PACKAGE_PATH)

    assert tp.package_name == ARGS_PACKAGE_NAME
    assert tp.package_path == RDS_PACKAGE_PATH

    assert ldr.package_name == ARGS_PACKAGE_NAME
    assert ldr.package_path == RDS_PACKAGE_PATH


def test_get_template_provider_rds():
    pp = ProviderPlugins()
    fstp = FileSystemTemplateProvider()
    ptp = PackageTemplateProvider()
    pp.providers.append(fstp)
    pp.providers.append(ptp)

    parser = ArgumentParser()
    cli_logg_util_setup_parser(parser)

    pp.update_arg_parser(parser)

    args = parser.parse_args(args=[])
    cli_logg_util_setup(args)
    pp.process_args(args)

    assert len(pp.active_providers) == 0
    rds = Json2AnyDescriptor(name='test_rds', template_location=RDS_PACKAGE_NAME,
                             template_provider='PackageTemplateProvider')
    tp: PackageTemplateProvider = pp.get_template_provider('rds_path', rds)
    assert tp == ptp

    ldr: PackageLoader = tp.get_loader(RDS_PACKAGE_PATH)
    assert tp.package_name == RDS_PACKAGE_NAME
    assert tp.package_path == RDS_PACKAGE_PATH

    assert ldr.package_name == RDS_PACKAGE_NAME
    assert ldr.package_path == RDS_PACKAGE_PATH