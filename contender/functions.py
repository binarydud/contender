from __future__ import print_function
import github3
import getpass
try:
    # Python 2
    prompt = raw_input
except NameError:
    # Python 3
    prompt = input


def integration_branch(repo, branch_name="integration"):
    integration = repo.ref('heads/{}'.format(branch_name))
    print(integration)
    master = repo.ref('heads/master')
    if integration:
        print('deleting ref')
        integration.delete()
    integration = repo.create_ref('refs/heads/{}'.format(branch_name), master.object.sha)
    # list_prs(repo)
    for pr in get_prs(repo, "master"):
        merge_pr(repo, integration.ref, pr)


def pr_from_numbers(repo, numbers):
    return [repo.pull_request(number) for number in numbers]


def list_prs(repo):
    pr_list = get_prs(repo, "master")
    chosen = choose_prs(pr_list)
    return chosen
    # print(choose_prs(get_prs(repo, "master")))


def create_release_candidate(repo, branch_name, pull_requests):
    # check and see if the rc exsists
    rc = repo.ref("heads/{}".format(branch_name))
    if rc:
        raise Exception('Release Candidate branch already exists')
    master = repo.ref('heads/master')
    rc = repo.create_ref('refs/heads/{}'.format(branch_name), master.object.sha)
    for pr in pull_requests:
        merge_pr(repo, rc.ref, pr)


def merge_pr(repo, base, pr):
    repo.merge(base, pr.head.sha)


def get_prs(repo, base):
    return list(repo.iter_pulls(base=base))


def format_pr(pr):
    return '{number}. - {message}'.format(number=pr.number, message=pr.title)


def prompt_for_pull_requests():
    return prompt('Choose the pull requests youd like: ')


def choose_prs(pr_list):
    map(print, map(format_pr, pr_list))
    results = prompt_for_pull_requests()
    return [item.strip() for item in results.split(',')]


def isvalid_pr(pr_number, pr_list):
    return pr_number in [pr.number for pr in pr_list]


def validate_config(config):
    # username
    assert 'user' in config
    # owner
    assert 'owner' in config
    # repository
    assert 'repository' in config
    # token
    assert 'token' in config

APP_NAME = 'contender'


def build_repo(user, token, owner, repository):
    gh = github3.login(
        user,
        token,
    )
    repo = gh.repository(owner, repository)
    return repo


def notify():
    print('Branch Built')


def read_config():
    pass
