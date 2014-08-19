import github3


class GithubBackend(object):
    def __init__(self, repo, config={}):
        self.repo = repo
        self.config = config

    @classmethod
    def build_repo(self, user, token, owner, repository):
        gh = github3.login(
            user,
            token,
        )
        repo = gh.repository(owner, repository)
        return repo

    def list_pull_requests(self):
        base_branch = self.config.get("base_branch", "master")
        pr_list = list(self.get_pull_requests(base_branch))
        return pr_list

    def get_branch(self, branch_name):
        branch = self.repo.ref('heads/{}'.format(branch_name))
        return branch

    def create_branch(self, branch_name, base_sha):
        return self.repo.create_ref('refs/heads/{}'.format(branch_name), base_sha)

    def delete_branch(self, branch_name):
        branch = self.get_branch(branch_name)
        branch.delete()

    def create_integration_branch(self, branch_name="integration"):
        branch = self.get_branch(branch_name)
        master = self.get_branch("master")
        if branch:
            branch.delete()
        integration = self.create_branch(branch_name, master.object.sha)

        base_branch = self.config.get("base_branch", "master")
        for pr in self.get_pull_requests(base_branch):
            self.merge_pull_request(integration.ref, pr)

    def create_release_candidate(self, branch_name, pull_requests):
        rc = self.get_branch(branch_name)
        if rc:
            raise Exception('Release Candidate branch already exists')
        master = self.get_branch("master")
        rc = self.create_branch(branch_name, master.object.sha)
        for pr in pull_requests:
            self.merge_pull_request(rc.ref, pr)

    def get_pull_requests(self, base="master"):
        return self.repo.iter_pulls(base=base)

    def merge_pull_request(self, base, pull_request):
        result = self.repo.merge(base, pull_request.head.sha)
        return result

    def format_pr(self, pull_request):
        return '{number}. - {message}'.format(
            number=pull_request.number,
            message=pull_request.title
        )

    def pull_request_from_number(self, number):
        return self.repo.pull_request(number)
