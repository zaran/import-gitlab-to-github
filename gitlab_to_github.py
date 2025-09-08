import os
import requests
import urllib.parse
import time
import argparse

# Config from env vars
SRC_GITLAB_URL = os.getenv("SRC_GITLAB_URL", "https://gitlab.school.edu")
SRC_TOKEN = os.getenv("SRC_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")  # your GitHub username
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not SRC_TOKEN or not GITHUB_USER or not GITHUB_TOKEN:
    raise SystemExit("Missing env vars: SRC_TOKEN, GITHUB_USER, GITHUB_TOKEN")

# GitLab session
s = requests.Session()
s.headers.update({"PRIVATE-TOKEN": SRC_TOKEN})

def get_gitlab_projects():
    """List projects from GitLab where you are a member."""
    url = f"{SRC_GITLAB_URL}/api/v4/projects"
    page, projects = 1, []
    while True:
        resp = s.get(url, params={"owned": True, "per_page": 100, "page": page})
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        projects.extend(data)
        page += 1
    return projects

def github_import(repo_name, clone_url, dry_run=False):
    if dry_run:
        print(f"[plan] Would create repo '{repo_name}' on GitHub and import from {clone_url}")
        return

    # Create repo
    create_url = "https://api.github.com/user/repos"
    r = requests.post(
        create_url,
        auth=(GITHUB_USER, GITHUB_TOKEN),
        json={"name": repo_name, "private": True},
    )
    if r.status_code not in (201, 422):  # 422 means already exists
        print(f"[error] creating repo {repo_name}: {r.text}")
        return

    # Start import
    import_url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/import"
    payload = {
        "vcs": "git",
        "vcs_url": clone_url,
        "vcs_username": "oauth2",
        "vcs_password": SRC_TOKEN,
    }
    r = requests.put(import_url, auth=(GITHUB_USER, GITHUB_TOKEN), json=payload)
    if r.status_code not in (201, 202):
        print(f"[error] importing {repo_name}: {r.text}")
    else:
        print(f"[ok] import started for {repo_name}")

def main():
    parser = argparse.ArgumentParser(description="Import GitLab projects into GitHub")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be imported without creating anything")
    args = parser.parse_args()

    projects = get_gitlab_projects()
    print(f"Found {len(projects)} projects on school GitLab\n")

    for pr in projects:
        repo_name = pr["path"]
        http_url = pr["http_url_to_repo"]

        parsed = urllib.parse.urlparse(http_url)
        clone_url = f"https://oauth2:{SRC_TOKEN}@{parsed.hostname}{parsed.path}"

        github_import(repo_name, clone_url, dry_run=args.dry_run)
        if not args.dry_run:
            time.sleep(0.5)  # gentle pacing

if __name__ == "__main__":
    main()
