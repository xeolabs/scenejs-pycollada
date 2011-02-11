SceneJS-PyCollada
=================

SceneJS-PyCollada is a small library / command-line utility for translating Collada files into
JSON formatted scenes for use by SceneJS. It uses PyCollada as its Collada
parser, hence the choice of name.

Supported features
==================

* None so far!

Building
========

You need to first install pycollada. Go into the directory that you've placed pycollada and run 

    python setup.py install

(Also see the pycollada README.markdown for more information on how to do this)

Updating pycollada
==================

PyCollada has been added to the project as a git submodule. To fetch the latest version of pycollada, you can use the following git command in the root directory of scenejs-pycollada.

    git submodule update

Resources
=========

For more information see the SceneJS website and wiki, or to discuss the project visit the google group.

GitHub project: [Google] [1]

Wiki page: [SceneJS Wiki page] [2]

Google group: [Google group] [3]

PyCollada home: [PyCollada] [4]

PyCollada: [PyCollada on GitHub] [5]

  [1]: https://github.com/xeolabs/scenejs-pycollada        "GitHub project"
  [2]: http://scenejs.wikispaces.com/scenejs-pycollada  "SceneJS Wiki page"
  [3]: http://groups.google.com/group/scenejs    "Google group"
  [4]: http://collada.in4lines.com/    "PyCollada"
  [5]: https://github.com/pycollada/pycollada    "PyCollada on GitHub"
