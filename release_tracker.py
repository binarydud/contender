from __future__ import print_function
import github3
import argparse
import re
import getpass
# import httplib
# httplib.HTTPConnection.debuglevel = 2
ticket_re = re.compile(r'(\w+)-(\d+)')
try:
    # Python 2
    prompt = raw_input
except NameError:
    # Python 3
    prompt = input


def my_two_factor_function():
    code = ''
    while not code:
        # The user could accidentally press Enter before being ready,
        # let's protect them from doing that.
        code = prompt('Enter 2FA code: ')
    return code


def login(username=None):
    if not username:
        user = prompt("Username [%s]: " % getpass.getuser())
        if not user:
            user = getpass.getuser()
    else:
        user = username

    password = getpass.getpass()
    return user, password


def parse_args():
    parser = argparse.ArgumentParser(description='Create release branch.')
    parser.add_argument('--user', '-U', help='user to authenticate as')
    parser.add_argument('owner', help='repo owner')
    parser.add_argument('repo', help='repositotry to check')
    parser.add_argument('--branch', help="branch to list", default='master')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    # user, passwd = login(args.user)
    user = 'binarydud'
    passwd = token
    gh = github3.login(
        user,
        passwd,
        two_factor_callback=my_two_factor_function
    )
    repo = gh.repository(args.owner, args.repo)
    # print [i.commit.message for i in repo.iter_commits(sha=args.branch, number=5)]
    # print [t.name for t in repo.iter_tags()]
    # print repo.tag('v3.0.1')
    integration_branch(repo)


def integration_branch(repo, branch_name="integration"):
    integration = repo.ref('heads/{}'.format(branch_name))
    print(integration)
    master = repo.ref('heads/master')
    if integration:
        print('deleting ref')
        integration.delete()
    print([(ref, ref.object.sha) for ref in repo.iter_refs()])
    integration = repo.create_ref('refs/heads/{}'.format(branch_name), master.object.sha)
    list_prs(repo)
    for pr in get_prs(repo, "master"):
        merge_pr(repo, integration.ref, pr)


def pr_from_number(number):
    return None


def pr_from_numbers(numbers):
    return filter(lambda x: x, map(pr_from_number, numbers))


def list_prs(repo):
    pr_list = get_prs(repo, "master")
    chosen = choose_prs(pr_list)
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


if __name__ == "__main__":
    main()
