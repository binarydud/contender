from __future__ import print_function
import pkg_resources


def validate_config(config):
    # username
    assert 'user' in config
    # owner
    assert 'owner' in config
    # repository
    assert 'repository' in config
    # token
    assert 'token' in config


def load_backend(config):
    dotted_path = config.get('backend', 'contender.backends.github:GithubBackend')
    Klass = pkg_resources.EntryPoint.parse("name={}".format(dotted_path)).load(False)

    repo = Klass.build_repo(config['user'], config['token'], config['owner'], config['repository'])
    return Klass(repo=repo, config=config)


def notify():
    print('Branch Built')
