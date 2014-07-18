Create "release branch":
    1. name branch
    2. get all open pull requests(check pr status for successful build)
    3. Allow user to choose prs
    4. given choices, merge pr into a rc branch
    5. create a pr for the release against the base branch
    6. tag all included prs as a part of the this release branch
    7. create a github release?

Create "integration" branch:
    note: remove any existing integration branches
    1. get all open pull requests(check pr status for successful build)
    2. for each pr, perform a merge: POST /repos/:owner/:repo/merges

Delete a release candidate:
    1. remove all rc tags from included pr
    2. close open pull request with message indicating this rc was failed
    2. delete rc branch

UI:
- create release branch
    - given a list of available prs, the user may choose which ones to merge
- create integration branch (special case of release branch where all positive prs are merged)

Ideas:
- abstract github into plugin architecture. 
- abstraction allows this to sit on top of its own git repo
- build web interface on top of the library
- filter commits/prs by commit status and mergeability (needs to be a clean merge)
- vendor/extend github3.py (take attributes in json and add to objects)
