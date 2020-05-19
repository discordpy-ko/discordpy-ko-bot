from github import Github
from git import Repo
import json

with open('botsetup.json', 'r', encoding="UTF-8") as f:
    bot_data = json.load(f)  # loads bot setups

g = Github(bot_data["github_token"])


async def get_gh_org(org_name: str):
    return g.get_organization(org_name)


async def get_gh_org_repo(org, repo_name: str):
    return org.get_repo(repo_name)


async def get_gh_repo(repo_name: str):
    return g.get_repo(repo_name)


async def clone_gh_repo(gh_repo, repo_folder: str):
    try:
        Repo.clone_from(gh_repo.clone_url, repo_folder)
    except:
        local_repo = Repo(repo_folder).remotes.origin
        local_repo.pull()


async def push_local_repo(repo_folder: str, msg: str):
    repo = Repo(repo_folder)
    repo.git.add(all=True)
    repo.index.commit(msg)
    web_o = repo.remotes.origin
    web_o.push()
