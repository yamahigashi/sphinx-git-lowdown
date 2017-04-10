sphinx-git-lowdown
==================

Installation
------------

conf.py
~~~~~~~

..  code:: python

    extensions = ['sphinx_git_lowdown']


use case sample
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

    .. git_release_logs::
        :search_path: Characters/001/*
        :release_tags: release-*
        :repository: C:/repository
        :max_count: 200

will be shown as

![sample](https://pbs.twimg.com/media/C8uM4L9V0AELAXa.jpg:large)


directive options
~~~~~~~~~~~~~~~~~~~~

search_path:
    git-rev-list command's paths option

release_tags:
    the release tag

repository:
    (optional) where repository is

max_count:
    (optional) maximum count of change logs
