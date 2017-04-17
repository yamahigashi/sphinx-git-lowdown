sphinx-git-lowdown
==================

An extension for the Sphinx_. That excerpt changelog with lowdown arrangement (https://pypi.python.org/pypi/Lowdown/0.1.1) from specified repository's git commit log.

.. _Sphinx: http://sphinx-doc.org/

Install
------------

.. code:: bat

    pip install -e git+https://github.com/yamahigashi/sphinx-git-lowdown.git#egg=sphinx_git_lowdown


conf.py
~~~~~~~

Add `sphinx_git_lowdown` to the extensions list in your project's conf.py.


.. code:: python

    extensions = ['sphinx_git_lowdown']


available directives
----------------------
- `git_release_logs`


- `git_change_logs`



option and sample
----------------------

**git_release_logs**

directive options:
~~~~~~~~~~~~~~~~~~~

::

  search_path:
      The git-rev-list command's paths option

  release_tags:
      The release tag

  repository:
      (optional) where repository is

  max_count:
      (optional) maximum count of change logs. (default: 200)

usage
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

    .. git_release_logs::
        :search_path: Characters/001/*
        :release_tags: release-*
        :repository: C:/repository
        :max_count: 200


will be shown as

.. image:: https://pbs.twimg.com/media/C8uM4L9V0AELAXa.jpg
  :alt: sample


**git_change_logs**

directive options:
~~~~~~~~~~~~~~~~~~~

::

    search_path:
        git-rev-list command's paths option
            
    repository:
        (optional) where repository is

    max_count:
        (optional) maximum count of change logs. (default: 200)

usage
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: rst

    .. git_change_logs::
        :search_path: Characters/001/*
        :repository: C:/repository
        :max_count: 200


will be shown as

.. image:: https://pbs.twimg.com/media/C8uM4L9V0AELAXa.jpg
  :alt: sample
