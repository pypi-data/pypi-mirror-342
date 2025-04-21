"""
Toolkit of programs/hooks for the ``pre-commit`` stage.
"""

from typing import Optional
import sys
import argparse

import git

from hooks._lib.git import (
    get_current_git_repo,
    get_active_branch,
)
from hooks._lib.gitlab import (
    GLIssueRef,
    get_gl_issue_ref_from_branch_name,
)


def safety_guard() -> None:
    """
    Prevents a commit to materialized if the staged changes contain a given safety guard phrase.

    This phrase is set by default to ``DO NOT COMMIT``, but can be changed by passing it as the
    first argument to this hook.

    It is case-sensitive and does not accept wildcards or regular expressions.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-g', '--guard-phrase', default='DO NOT COMMIT')
    args = parser.parse_args()
    guard_phrase: str = args.guard_phrase
    failed_job: bool = False
    this_repo: git.Repo = get_current_git_repo()
    staged_blobs = this_repo.index.diff(this_repo.head.commit, create_patch=True)
    for staged_blob in staged_blobs:
        if staged_blob.a_blob:
            try:
                new_blob: str = staged_blob.a_blob.data_stream.read().decode('utf-8')
                if guard_phrase in new_blob:
                    print(
                        f'File {staged_blob.a_path} contains guard phrase '
                        f'"{guard_phrase}":\n{new_blob}'
                    )
                    failed_job = True
            except UnicodeDecodeError:
                # Ignore binary files
                pass

    if failed_job:
        print('Some changes in the stage are marked as protected from committing')
        sys.exit(1)

def enforce_committing_to_issue() -> None:
    """
    Enforce changes are only committed to issue branches.
    """
    active_branch_name: Optional[str] = get_active_branch()
    if not active_branch_name:
        print('An active branch could not be determined from the current directory')
        sys.exit(1)

    # TODO: Support other formats like GL-xxx
    branch_issue_ref: Optional[GLIssueRef] = get_gl_issue_ref_from_branch_name(active_branch_name)
    if not branch_issue_ref:
        print(
            f'Branch "{active_branch_name}" does not seem to be an issue branch. '
            'Changes must be committed to issue branches only.'
        )
        sys.exit(1)
