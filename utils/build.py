import os


def build_docs():
    os.system("sphinx-build -b html discord.py-master/docs docsweb")


if __name__ == "__main__":
    os.chdir("../")
    build_docs()
