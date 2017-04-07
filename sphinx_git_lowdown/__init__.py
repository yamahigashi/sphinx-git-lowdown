# -*- coding: utf-8 -*-

import sys
import six
import git

import fnmatch
from datetime import datetime

import docutils
from docutils.statemachine import StringList, ViewList
from sphinx.util.compat import Directive

import lowdown


reload(sys)
sys.setdefaultencoding('UTF8')


class Release(object):
    """represent release object"""

    def __init__(self):
        # type: () -> None
        self.changesets = []  # type: list[Changeset]

    def set_date(self, date):
        # type: (datetime) -> None

        self.date = date

    def set_version(self, version):
        # type: (str) -> None

        if version is not None:
            self.version = version

        else:
            self.version = ""

    def add_change(self, changeset):
        # type: (Changeset) -> None
        self.changesets.append(changeset)

    def add_changes(self, changesets):
        # type: (list[Changeset]) -> None

        for c in changesets:
            self.add_change(c)

    def to_content(self):
        # type: () -> str
        res = StringList()

        for change in self.changesets:
            res.append(change.to_content())
            res.append(ViewList([u""]))

        return res


class Changeset(object):
    """represent each change"""

    def __init__(self, date, message, files):
        # type: (datetime, str, list[str]) -> None

        self.date = date
        self.message = message
        self.files = files

        self.set_status_from_message(self.message)
        self.set_tags_from_message(self.message)

    def set_category(self, category):
        # type: (str) -> None
        self.category = category.encode("utf8")  # possibly: ["changed", "new", "fixed"]

    def set_tags(self, tags):
        # type: (list[str]) -> None

        self.tags = []  # type: list[unicode]

        for tag in tags:
            tag = tag.encode("utf8")
            self.tags.append(tag)

    def set_status_from_message(self, message):
        # type: (str) -> None
        self.category = "other"  # possibly: ["changed", "new", "fixed"]

    def set_tags_from_message(self, message):
        # type: (str) -> None
        self.tags = ["general"]

    def to_content(self):
        # type: () -> StringList

        content = StringList()
        content.append(ViewList([u".. change:: {}".format(self.category)]))
        content.append(ViewList([u"    :tags: {}".format(",".join(self.tags))]))
        content.append(ViewList([u""]))
        content.append(ViewList([u"    {}".format(self.message)]))

        return content


class GitLogBase(Directive):
    '''The base class'''

    def _find_repository(self):
        # type: () -> git.Repo

        repo_dir = self.options.get("repository", None)
        if not repo_dir:
            repo_dir = self.state.document.settings.env.srcdir

        repo = git.Repo(repo_dir, search_parent_directories=True)

        return repo

    def _get_commits(self):
        # type:  () -> list[git.objects.commit.Commit]

        query_opt = {
            "rev": None,
            "paths": self.options.get('search_path', None),
            "max_count": self.options.get('max_count', 200)
        }

        commits = self.repository.iter_commits(**query_opt)
        return list(commits)

    def _get_tags(self, commits):
        # type:  (list[git.objects.commit.Commit]) -> list[git.refs.tag.TagReference]

        def _match_tag(tag_name):
            # type: (str) -> bool

            for tag in self.options.get("release_tags", []):
                if fnmatch.fnmatchcase(tag_name, tag):
                    return True

            return False

        tags = [x for x in self.repository.tags]
        tags.sort(key=lambda x: x.tag.tagged_date, reverse=True)
        tags = [x for x in tags if _match_tag(x.name)]

        return self._filter_tag(tags, commits)

    def _filter_tag(self, tags, commits):
        # type: (list[git.refs.tag.TagReference], list[git.objects.commit.Commit]) -> list[git.refs.tag.TagReference]
        """Filter tag that does not contain any commit."""

        def _is_contain(tag):
            # type: (git.refs.tag.TagReference) -> bool
            for c in commits:
                if c == tag.commit:
                    return True

            return False

        return [tag for tag in tags if _is_contain(tag)]

    def _extract_changed_files(self, commit):
        # type: (git.objects.commit.Commit) -> list[str]

        changed = []  # type: list[str]

        def append(x):
            if x.a_blob is not None and x.a_blob.path not in changed:
                changed.append(x.a_blob.path)
                # print "a", x.a_blob.path

            if x.b_blob is not None and x.b_blob.path not in changed:
                changed.append(x.b_blob.path)
                # print "b", x.b_blob.path

        try:
            for x in commit.diff(commit.parents[0]):
                append(x)

        except IndexError:
            pass

        return changed


class GitReleaseChangelog(GitLogBase):
    '''Git Release log directive.

    Mark a releases and changes in the repository. Releases should be specified
    with string that is part of git tag name::

        .. git_release_logs
            :search_path: - A path to limit the returned commits to display
            :release_tags: - Tag matching patterns used with fnmatch to display
            :repository: - (optional) A repository inspected into. (default: The source directory)
            :max_count: - (optional) A revision count that is displayed. (default: 200)

    '''

    has_content = False
    option_spec = {
        'search_path': six.text_type,
        'release_tags': lowdown.comma_separated_list,
        'repository': six.text_type,
        'max_count': docutils.parsers.rst.directives.nonnegative_int
    }

    def run(self):
        # type: () -> list[list[docutils.nodes.Element]]

        self.repository = self._find_repository()

        commits = self._get_commits()
        tags = self._get_tags(commits)
        releases = self._split_commits_by_tag(commits, tags)

        nodes = self._run_internal_directive(releases)

        return nodes

    def _run_internal_directive(self, releases):
        # type: (list[Release]) -> list[list[docutils.nodes.Element]]

        res = []  # type: list[list[docutils.nodes.Element]]

        for rel in releases:

            # release, run lowdown directive

            name = self.name
            arguments = [rel.version, ]  # arguments
            options = {"date": rel.date}  # options
            content = rel.to_content()
            lineno = self.lineno
            content_offset = self.content_offset
            block_text = u""  # block_text
            state = self.state
            state_machine = self.state_machine

            release = lowdown.ReleaseDirective(
                name, arguments, options, content, lineno, content_offset,
                block_text, state, state_machine
            )

            r_entry = release.run()
            res.extend(r_entry)

        return res

    def _split_commits_by_tag(self, commits, tags):
        # type: (list[git.objects.commit.Commit], list[git.refs.tags.TagReference]) -> list[Release]

        releases = []

        current_release = None
        publish_releases = tags
        next_cursor = publish_releases.pop(0)
        version = next_cursor.name

        while commits[0].committed_datetime < next_cursor.commit.committed_datetime:
            if publish_releases:
                next_cursor = publish_releases.pop(0)

            else:
                break

        def _is_match_version(commit, cursor):
            # type: (git.objects.commit.Commit, git.refs.tag.TagReference) -> bool
            if not cursor:
                return False

            return commit == cursor.commit

        for commit in commits:

            if _is_match_version(commit, next_cursor):

                date = datetime.fromtimestamp(commit.authored_date)

                current_release = Release()
                current_release.set_date(date)
                current_release.set_version(version)
                releases.append(current_release)

                if publish_releases:
                    next_cursor = publish_releases.pop(0)
                    version = next_cursor.name

                else:
                    next_cursor = None

            if current_release is not None:
                message = commit.message
                changed = self._extract_changed_files(commit)
                changes = tokenize_commit_message_into_changeset(date, message, changed)
                current_release.add_changes(changes)

        if not releases:
            print("no releases found in this current active branch: {}".format(
                self.repository.active_branch.name
            ))

        return releases


class GitChangelog(GitLogBase):
    '''Git log directive.

    Mark a releases and changes in the repository. Releases should be specified
    with string that is part of git tag name::

        .. git_release_logs
            :search_path: - A path to limit the returned commits to display
            :repository: - (optional) A repository inspected into. (default: The source directory)
            :max_count: - (optional) A revision count that is displayed. (default: 200)

    '''

    has_content = False
    option_spec = {
        'search_path': six.text_type,
        'repository': six.text_type,
        'max_count': docutils.parsers.rst.directives.nonnegative_int
    }

    def run(self):
        # type: () -> list[list[docutils.nodes.Element]]

        self.repository = self._find_repository()

        commits = self._get_commits()
        changes = self._generate_changesets(commits)

        nodes = self._run_internal_directive(changes)

        return nodes

    def _run_internal_directive(self, rel):
        # type: (Release) -> list[list[docutils.nodes.Element]]

        res = []  # type: list[list[docutils.nodes.Element]]

        name = self.name
        arguments = [rel.version, ]  # arguments
        options = {"date": rel.date}  # options
        content = rel.to_content()
        lineno = self.lineno
        content_offset = self.content_offset
        block_text = u""  # block_text
        state = self.state
        state_machine = self.state_machine

        release = lowdown.ReleaseDirective(
            name, arguments, options, content, lineno, content_offset,
            block_text, state, state_machine
        )

        r_entry = release.run()
        res.extend(r_entry)

        return res

    def _generate_changesets(self, commits):
        # type: (list[git.objects.commit.Commit]) -> Release

        changesets = []

        for commit in commits:

            date = datetime.fromtimestamp(commit.authored_date)
            message = commit.message
            changed = self._extract_changed_files(commit)
            changes = tokenize_commit_message_into_changeset(date, message, changed)

            changesets.extend(changes)

        if not changesets:
            print("no changesets found in this current active branch: {}".format(
                self.repository.active_branch.name
            ))

        container_release = Release()
        container_release.set_date(datetime.fromtimestamp(commits[0].authored_date))
        container_release.set_version(self.options.get("name", ""))
        container_release.add_changes(changesets)

        return container_release


def tokenize_commit_message_into_changeset(date, message, changed):
    # type: (datetime, str, list[str]) -> list[Changeset]

    res = []

    lines = message.split("\n")
    message = ""
    cat = ""
    tags = []  # type: list[str]
    for line in lines:

        if line.startswith("category:"):
            cat = line.split("category:")[-1].strip()

        elif line.startswith("tags:"):
            tags = line.split("tags:")[-1].strip().split(",")

        elif line.strip() == "":
            change = Changeset(date, message, changed)

            if cat:
                change.set_category(cat)

            if tags:
                change.set_tags(tags)

            res.append(change)

            # refresh to blank, preparing for new changeset
            message = ""
            cat = ""
            tags = []

        else:
            message = message + line

    return res


def setup(app):
    app.add_directive('git_release_logs', GitReleaseChangelog)
    app.add_directive('git_change_logs', GitChangelog)
