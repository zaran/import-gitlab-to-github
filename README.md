# import-gitlab-to-github
Import GitLab repos into GitHub

Need these creds:
```
SRC_GITLAB_URL="https://gitlab.school.edu"
SRC_TOKEN="school_gitlab_pat"
GITHUB_USER="your_github_username"
GITHUB_TOKEN="your_github_pat"
```

Usage:
```
usage: gitlab_to_github.py [-h] [--dry-run]

Import GitLab projects into GitHub

options:
  -h, --help  show this help message and exit
  --dry-run   Show what would be imported without creating anything
```

Edit: Turns out the endpoint to import repos has been deprecated :(

I got this error:
```
[error] importing [REPO-NAME]: {"message":"This endpoint has been deprecated. To import a repository, please use the GitHub Importer tool at https://github.com/new/import.","documentation_url":"https://docs.github.com/rest","status":"404"}
```


The "dry-run" arg is still useful to get the list of repo URLs to import.
