"""
Utility functions for git-related operations.
"""

from typing import Optional

import git


def get_current_git_repo() -> Optional[git.Repo]:
    """
    Gets the git repo at the current working directory.

    :return: The git repo if currently in a cloned git repo; ``None`` otherwise.
    :rtype: Optional[git.Repo]
    """
    try:
        return git.Repo('.')
    except git.exc.InvalidGitRepositoryError:
        print('Looks like the current directory is not in a git repo')
        return None

def get_active_branch() -> Optional[str]:
    """
    Gets the currently active branch in the current git repo.

    :return: The active branch name if in a repo with a non-detached HEAD; ``None`` otherwise.
    :rtype: Optional[str]
    """
    this_repo: Optional[git.Repo] = get_current_git_repo()
    if not this_repo:
        return None
    try:
        return this_repo.active_branch.name
    except TypeError:
        print('Current repo is in a detached state')
        return None

def read_commit_msg(commit_msg_filename: str) -> str:
    """
    Reads the commit message file to a string.

    :param commit_msg_filename: The commit message file name.
    :type commit_msg_filename: str
    :return: The commit message as a string.
    :rtype: str
    """
    with open(commit_msg_filename, "rt", encoding='utf-8') as commit_msg_file:
        return commit_msg_file.read()

def write_commit_msg(commit_msg_filename: str, commit_msg: str) -> None:
    """
    Writes a string into a commit message file.

    :param commit_msg_filename: The commit message filename.
    :type commit_msg_filename: str
    :param commit_msg: The commit message to write.
    :type commit_msg: str
    """
    with open(commit_msg_filename, "wt", encoding='utf-8') as commit_msg_file:
        commit_msg_file.write(commit_msg)

def get_commit_message_subject(commit_msg: str) -> str:
    """
    Extracts the subject from the commit message.

    :param commit_msg: The commit message.
    :type commit_msg: str
    :return: The commit message subject.
    :rtype: str
    """
    return commit_msg.partition('\n')[0]


__all__ = [
    'get_current_git_repo',
    'get_active_branch',
    'read_commit_msg',
    'write_commit_msg',
    'get_commit_message_subject',
]
