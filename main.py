from dotenv import load_dotenv
from enum import Enum
import datetime
import shutil
import git
import sys
import os
import re


# config
load_dotenv(override=True)
class Config(Enum):
    REPOSITORY = str(os.getenv('REPOSITORY_URL'))
    ORIGINAL_DIR = str(os.getenv('ORIGINAL_DIR'))
    BACKUP_DIR = str(os.getenv('BACKUP_DIR')) if os.getenv('BACKUP_DIR') is not None else 'backup'
    BACKUP_USER = re.sub(r' ', '', str(os.getenv('BACKUP_USER'))).split(',') if os.getenv('BACKUP_USER') is not None else []
    FLOW_DIR = BACKUP_DIR + '/flow_service'


# methods
def get_date():
    t_delta = datetime.timedelta(hours=9)
    jst = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(jst)
    return '%s %s' % (now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S'))


# init
def init():
    # check dir
    os.makedirs(Config.FLOW_DIR.value, exist_ok=True)

    # git init and create remote
    repo = git.Repo.init(Config.BACKUP_DIR.value)
    if 'origin' not in map(lambda r: r.name, repo.remotes):
        remote = repo.create_remote(name='origin', url=Config.REPOSITORY.value)
        print(remote)

    print('initialization ok!')


# backup
def backup_flow_service():
    # remove folder
    shutil.rmtree(Config.FLOW_DIR.value)

    # backup flow service
    user_list = os.listdir(f"{Config.ORIGINAL_DIR.value}/home")
    print(f"backup user: {Config.BACKUP_USER.value}")

    # flow file
    for user in user_list:
        if user in Config.BACKUP_USER.value:
            shutil.copytree(f"{Config.ORIGINAL_DIR.value}/home/{user}", f"{Config.FLOW_DIR.value}/home/{user}")

    # schedule data
    shutil.copytree(f"{Config.ORIGINAL_DIR.value}/data", f"{Config.FLOW_DIR.value}/data")


def generate_readme_and_ignore_file():
    date = get_date()
    user_list = ''

    for user in Config.BACKUP_USER.value:
        user_list += f"- {user}\n"

    readme = open('template/README.md', 'r', encoding="utf-8")
    text = readme.read()
    readme.close()

    text = text.replace('{date}', date)
    text = text.replace('{user_list}', user_list)

    # create README.md
    with open('%s/README.md' % (Config.BACKUP_DIR.value), 'w') as file:
        file.write(text)

    # create .gitignore
    shutil.copy('template/.gitignore', f"{Config.BACKUP_DIR.value}/.gitignore")


def git_commit_and_push(mode):
    message = 'backup: %s' % (get_date())

    # git commit
    repo = git.Repo(Config.BACKUP_DIR.value)
    repo.git.add('.')
    commit = repo.git.commit('.', message=message)
    print(commit)
    if mode != 'local':
        push = repo.git.push('origin', 'master')
        print(push)

    print('commit and push ok!')


# main
def main():
    # initializaion
    init()

    # backup
    backup_flow_service()

    # generate README.md
    generate_readme_and_ignore_file()

    # commit and push
    try:
        mode = sys.argv[1]
    except IndexError as e:
        mode = ""

    git_commit_and_push(mode)


if __name__ == '__main__':
    main()

