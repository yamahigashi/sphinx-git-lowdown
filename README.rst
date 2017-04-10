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

.. raw:: html

  <div class="section" id="id3">
  <h2>更新履歴<a class="headerlink" href="#id3" title="このヘッドラインへのパーマリンク">¶</a></h2>
  <div class="lowdown-release section" id="release-release-01.03.00">
  <h3><span>release-01.00.00</span><a class="headerlink" href="#release-release-00.00.01" title="このヘッドラインへのパーマリンク">¶</a></h3>
  <em class="release-date">2017-04-07</em><ul class="lowdown-change-list">
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-other">other</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-general">general</span>wip</p>
  </div>
   </div>
  </li>
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-new">new</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-機能">機能</span>頭、首の FK/IK 切り替え機能に、プロット機能追加</p>
  </div>
   </div>
  </li>
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-new">new</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-機能">機能</span>左手のIK親空間切り替え先に武器を追加</p>
  </div>
   </div>
  </li>
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-fixed">fixed</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-body">body</span><cite>cog</cite> が骨に <strong>つながっていなかった</strong></p>
  </div>
   </div>
  </li>
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-changed">changed</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-body">body</span>モデル変更に合わせコントローラの位置を調整</p>
  </div>
   </div>
  </li>
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-other">other</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-モデル">モデル</span>モデルを仮モデルから入れ替え</p>
  </div>
   </div>
  </li>
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-fixed">fixed</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-スキニング">スキニング</span>腕を修正</p>
  </div>
   </div>
  </li>
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-new">new</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-一般">一般</span>新規追加</p>
  </div>
   </div>
  </li>
  </ul>
  </div>
  <div class="line-block">
  <div class="line"><br /></div>
  </div>
  </div>
  <div class="lowdown-release section" id="release-release-00.00.01">
  <h3><span>release-00.03.11</span><a class="headerlink" href="#release-release-20170308-02-01-04" title="このヘッドラインへのパーマリンク">¶</a></h3>
  <em class="release-date">2017-04-06</em><ul class="lowdown-change-list">
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-fixed">fixed</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-body">body</span>腕 ik fk 切り替え時の rot_ctl 未反映修正</p>
  </div>
   </div>
  </li>
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-fixed">fixed</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-body">body</span>足 ik fk 切り替え時の つま先未追従修正</p>
  </div>
   </div>
  </li>
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-other">other</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-general">general</span>wip</p>
  </div>
   </div>
  </li>
  <li><div class="lowdown-change first">
  <span class="lowdown-category lowdown-category-other">other</span> <div class="docutils container">
  <p><span class="lowdown-tag lowdown-tag-general">general</span>足のUPVを修正</p>
  </div>
   </div>
  </li>
  </ul>
  </div>
  </div>



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
