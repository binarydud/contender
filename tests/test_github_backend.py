import pytest
import github3
try:
    from unittest import mock
except:
    import mock
from pretend import stub
from github3.repos.repo import Repository

from contender.backends import GithubBackend


def build_url(self, *args, **kwargs):
    # We want to assert what is happening with the actual calls to the
    # Internet. We can proxy this.
    return github3.session.GitHubSession().build_url(*args, **kwargs)


def create_mocked_session():
    MockedSession = mock.create_autospec(github3.session.GitHubSession)
    return MockedSession()


def create_session_mock(*args):
    session = create_mocked_session()
    base_attrs = ['headers', 'auth']
    attrs = dict(
        (key, mock.Mock()) for key in set(args).union(base_attrs)
    )
    get_response = stub(
        status_code=200,
        headers={},
        content={},
    )
    session.configure_mock(**attrs)
    session.delete.return_value = None
    session.get.return_value = get_response
    session.patch.return_value = None
    session.post.return_value = None
    session.put.return_value = None
    return session


@pytest.fixture()
def repo():
    repo = Repository({"url": "https://api.github.com/repos/binarydud/mock-contender"}, session=create_session_mock())
    repo._build_url = build_url
    return repo


@pytest.fixture()
def backend(repo):
    return GithubBackend(repo)


def test_list_pull_requests(backend):
    backend.list_pull_requests()
    backend.repo._session.get.assert_called_once_with(
        'https://api.github.com/repos/binarydud/mock-contender',
        headers={},
        params={'sort': u'created', 'per_page': 100, 'direction': u'desc', 'base': 'master'}
    )


def test_get_branch(backend):
    backend.get_branch("test")
    backend.repo._session.get.assert_called_once_with('https://api.github.com/repos/binarydud/mock-contender/refs/heads/test')


def test_create_branch(backend):
    backend.create_branch("test-branch", 12345)
    backend.repo._session.post.assert_called_once_with(
        'https://api.github.com/repos/binarydud/mock-contender/refs',
        '{"sha": 12345, "ref": "refs/heads/test-branch"}'
    )


@pytest.mark.xfail
def test_delete_branch(backend):
    backend.delete_branch('test-branch')


@pytest.mark.xfail
def test_create_integration_branch(backend):
    backend.create_integration_branch()
    backend.repo._session.post.assert_called_once_with(
        'https://api.github.com/repos/binarydud/mock-contender/refs',
        '{"sha": 12345, "ref": "refs/heads/test-branch"}'
    )


@pytest.mark.xfail
def test_create_release_candidate(backend):
    backend.create_release_candidate("rc-test", [])


def test_get_pull_requests(backend):
    iterator = backend.get_pull_requests()
    assert iterator
    assert isinstance(iterator, github3.structs.GitHubIterator)


def test_merge_pull_request(backend):
    pr = stub(head=stub(sha=123))
    backend.merge_pull_request("base", pr)
    backend.repo._session.post.assert_called_once_with(
        'https://api.github.com/repos/binarydud/mock-contender',
        '{"head": 123, "base": "base"}'
    )


def test_format_pr(backend):
    pr = stub(number=1, title="Commit Message")
    assert backend.format_pr(pr) == "1. - Commit Message"


def test_pull_request_from_number(backend):
    backend.pull_request_from_number(1)
    backend.repo._session.get.assert_called_once_with(
        'https://api.github.com/repos/binarydud/mock-contender/1',
    )
