import os
import shutil
import json
import git
import github


def build_docs(msg: str):
    with open('bot_settings.json', 'r', encoding="UTF-8") as f:
        bot_settings = json.load(f)
    g = github.Github(bot_settings["github_token"])
    repo_list = ["discord.py-docs-kor-project", "discordpy-ko.github.io"]
    for x in repo_list:
        _repo = g.get_organization("discordpy-ko").get_repo(x)
        try:
            git.Repo.clone_from(_repo.clone_url, x)
        except: # 예외가 뭐 뜨는지 확인하기 귀찮아요
            local_repo = git.Repo(x).remotes.origin
            local_repo.pull()
    shutil.rmtree("discord.py-master/docs/locale")
    shutil.copytree("discord.py-docs-kor-project/locale", "discord.py-master/docs/locale")
    existing_files = os.listdir("docsweb")
    if len(existing_files) > 0:
        [shutil.rmtree("docsweb/"+x) if x == ".doctrees" or "." not in x else os.remove("docsweb/"+x) for x in existing_files]
    if os.path.isfile("build_log.txt"):
        os.remove("build_log.txt")
    open("build_log.txt", "w").close()
    orig_dir = os.getcwd()
    os.chdir("discord.py-master/docs")
    os.system(f"sphinx-build -b html ./ {orig_dir}/docsweb -w {orig_dir}/build_log.txt")
    os.chdir(orig_dir)
    if os.path.isdir("docsweb/html"):
        base_dir = "docsweb/html"
    else:
        base_dir = "docsweb"
    for x in os.listdir(base_dir):
        if x == "_static":
            [os.remove("discordpy-ko.github.io/_static/"+n) for n in os.listdir("discordpy-ko.github.io/_static") if n != "style.css"]
            for y in os.listdir(base_dir+"/_static"):
                if y != "style.css":
                    shutil.move(base_dir + "/_static/" + y, "discordpy-ko.github.io/_static/" + y)
            continue
        if x in os.listdir("discordpy-ko.github.io"):
            shutil.rmtree("discordpy-ko.github.io/" + x) if x == ".doctrees" or "." not in x else os.remove("discordpy-ko.github.io/" + x)
        shutil.move(base_dir+"/"+x, "discordpy-ko.github.io/"+x)
    repo = git.Repo("discordpy-ko.github.io")
    repo.git.add(all=True)
    repo.index.commit(msg)
    web_o = repo.remotes.origin
    web_o.push()


"""
if __name__ == "__main__":
    os.chdir("../")
    build_docs()
"""
