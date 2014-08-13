import collections
import click
from ConfigParser import SafeConfigParser

# from functions import *
from functions import (
    validate_config,
    build_repo,
    list_prs,
    integration_branch,
    notify,
    pr_from_numbers,
    create_release_candidate,
    get_prs
)


class Contender(object):
    def __init__(self):
        self.config = {}

    def set_config(self, key, value):
        self.config[key] = value

pass_config = click.make_pass_decorator(Contender)


@click.group()
# @click.option('--user')
# @click.option('--repository')
# @click.option('--token')
# @click.option('--owner')
@click.option('--config')
@click.pass_context
def contender(ctx, **kwargs):
    ctx.obj = Contender()
    config_file = click.get_app_dir('contender', force_posix=True)
    config_parser = SafeConfigParser()
    config = kwargs['config']
    if config:
        config_file = config
    config_parser.read(config_file)
    if 'contender' in config_parser.sections():
        for key, value in config_parser.items('contender'):
            ctx.obj.set_config(key, value)

    # if kwargs['user']:
    #     ctx.obj.set_config("user", kwargs["user"])
    # if kwargs['repository']:
    #     ctx.obj.set_config("repository", kwargs["repository"])
    if ctx.invoked_subcommand != 'init':
        try:
            validate_config(ctx.obj.config)
        except AssertionError:
            raise click.UsageError('Incomplete configuration', ctx)


@contender.command()
@pass_config
def integration(contender):
    config = contender.config
    repo = build_repo(config['user'], config['token'], config['owner'], config['repository'])
    integration_branch(repo)
    notify()


@contender.command()
@click.argument("release_branch")
@pass_config
def release_candidate(contender, release_branch):
    config = contender.config
    repo = build_repo(config['user'], config['token'], config['owner'], config['repository'])
    pr_numbers = list_prs(repo)
    pr_list = pr_from_numbers(repo, pr_numbers)
    create_release_candidate(repo, release_branch, pr_list)
    notify()


@contender.command()
@click.argument("release_branch")
@pass_config
def merge_release(contender, release_branch):
    config = contender.config
    repo = build_repo(config['user'], config['token'], config['owner'], config['repository'])
    # Perform a merge from head into base
    repo.merge("master", release_branch, 'merging from contender tool')
    # prune release branch
    release_branch = repo.ref("heads/{}".format(release_branch))
    release_branch.delete()
    # TODO - prune pr branches
    # pull_requests = get_prs(repo, "master")


@contender.command()
@click.argument("branch")
@pass_config
def delete_branch(contender, branch):
    config = contender.config
    repo = build_repo(config['user'], config['token'], config['owner'], config['repository'])
    branch = repo.ref('heads/{}'.format(branch))
    branch.delete()


@contender.command()
def delete_release():
    pass


@contender.command()
def init():
    user = raw_input('what is the username to connect to: ')
    token = raw_input('the token to use for communicating to the github api: ')
    repository = raw_input('repository the work will be done on: ')
    owner = raw_input('who owns the repository: ')
    config_file = click.get_app_dir('contender', force_posix=True)

    config = SafeConfigParser()
    config.add_section('contender')
    config.set('contender', 'user', user)
    config.set('contender', 'token', token)
    config.set('contender', 'repository', repository)
    config.set('contender', 'owner', owner)
    with open(config_file, 'wb') as configfile:
        config.write(configfile)


# if __name__ == "__main__":
#    contender(obj={"contender": {}})
