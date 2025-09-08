# import-gitlab-to-githb
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
