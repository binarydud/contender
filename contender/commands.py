from __future__ import print_function

import click
from six.moves import configparser

try:
    # Python 2
    prompt = raw_input
except NameError:
    # Python 3
    prompt = input

# from functions import *
from contender.utils import (
    validate_config,
    load_backend,
    notify,
)


class Contender(object):
    def __init__(self, backend=None):
        self.config = {}
        if backend:
            self.backend = backend

    def set_config(self, key, value):
        self.config[key] = value

pass_config = click.make_pass_decorator(Contender)


@click.group()
@click.option('--config')
@click.pass_context
def contender(ctx, config):
    ctx.obj = Contender()
    config_file = click.get_app_dir('contender', force_posix=True)
    config_parser = configparser.SafeConfigParser()
    if config:
        config_file = config
    config_parser.read(config_file)
    if 'contender' in config_parser.sections():
        for key, value in config_parser.items('contender'):
            ctx.obj.set_config(key, value)

    if ctx.invoked_subcommand != 'init':
        try:
            validate_config(ctx.obj.config)
        except AssertionError:
            raise click.UsageError('Incomplete configuration', ctx)

    ctx.obj.backend = load_backend(ctx.obj.config)


@contender.command()
@pass_config
def integration(contender):
    backend = contender.backend
    backend.create_integration_branch()
    notify()


@contender.command()
@click.argument("release_branch")
@pass_config
def release_candidate(contender, release_branch):
    backend = contender.backend
    map(print, backend.get_pull_requests())
    results = prompt('Choose the pull requests youd like: ')
    pr_numbers = [item.strip() for item in results.split(',')]

    pull_requests = map(backend.pull_request_from_number, pr_numbers)
    backend.create_release_candidate(release_branch, pull_requests)
    notify()


@contender.command()
@click.argument("release_branch")
@pass_config
def merge_release(contender, release_branch):
    backend = contender.backend
    # Perform a merge from head into base
    backend.repo.merge("master", release_branch, 'merging from contender tool')
    # prune release branch
    release_branch = backend.repo.ref("heads/{}".format(release_branch))
    release_branch.delete()
    # TODO - prune pr branches
    # pull_requests = get_prs(repo, "master")


@contender.command()
@click.argument("branch")
@pass_config
def delete_branch(contender, branch):
    backend = contender.backend
    backend.delete_branch(branch)


@contender.command()
def init():
    user = prompt('what is the username to connect to: ')
    token = prompt('the token to use for communicating to the github api: ')
    repository = prompt('repository the work will be done on: ')
    owner = prompt('who owns the repository: ')
    config_file = click.get_app_dir('contender', force_posix=True)

    config = configparser.SafeConfigParser()
    config.add_section('contender')
    config.set('contender', 'user', user)
    config.set('contender', 'token', token)
    config.set('contender', 'repository', repository)
    config.set('contender', 'owner', owner)
    with open(config_file, 'wb') as configfile:
        config.write(configfile)
