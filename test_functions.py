from pretend import stub


def test_format_pr():
    from release_tracker import format_pr
    pr = stub(number=1, title='Commit Message')
    assert format_pr(pr) == '1. - Commit Message'
