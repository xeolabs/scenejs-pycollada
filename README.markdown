SceneJS-PyCollada
=================

SceneJS-PyCollada is a small library / command-line utility for translating Collada files into
JSON formatted scenes for use by SceneJS. It uses PyCollada as its Collada
parser, hence the choice of name.

Licensing
=========

SceneJS-PyCollada is dual licensed under the MIT license and GPL version 2.0. Please refer to the files under licenses/ for more information.
PyCollada is licensed under a BSD-style license. Please see pycollada/COPYING for more information

Features
========

* Loads the following geometry nodes: <polylist>, <triangles>, <lines>
** However, it is still missing the following: <polygons>
* Supports vertex splitting when a shared vertex has conflicting attributes. (This is required for flat shading or split texture coordinates for example)
* Import multiple primitive types in one mesh using subgeometries
* Supports the following vertex attributes: 
** Positions
** Normals
** Texture coordinates (one set only at the moment)
* Loads the following light nodes: <point>, <directional>
* Loads basic materials (no shaders yet)
* Generates sample files (html + javascript)

Please test and report bugs!

Work in progress
================

* Pretty printing for javascript files
* Ambient light sources (not supported by SceneJS yet)
* Point light sources (it is not known to what extent these work currently)
* Multiple subgeometries (this is mostly implemented, but doesn't seem to work in SceneJS for some reason)

Installing python
=================

There's a good chance that you already have python, however if you don't, visit http://python.org and get it!

Updating pycollada
==================

PyCollada has been added to the project as a git submodule. To fetch the latest version of pycollada, you can use the following git command in the root directory of scenejs-pycollada.

    git submodule update --init

PyCollada depends on the NumPy module. If you're on a unixy platform there's a good chance that you'll already have NumPy and you can skip this step.

However, if you don't have NumPy installed on your system, fetch an appropriate release from the NumPy website, http://numpy.scipy.org (http://www.scipy.org/Download has the list of all builds including unofficial releases)
Note that on 64bit windows you'll most likely need to fetch an unofficial build of NumPy from http://www.lfd.uci.edu/~gohlke/pythonlibs/

Building
========

You need to first install pycollada. Go into the directory that you've placed pycollada and run 

    python setup.py install

(Also see the pycollada README.markdown for more information on how to do this)

Installing and running scenejs-pycollada
========================================

scenejs-pycollada is not installable currently, however you can simply run it directly.

This command will give you the usage information you need to run the utility:

    python scenejs-pycollada --help


Resources
=========

For more information see the SceneJS website and wiki, or to discuss the project visit the google group.

GitHub project: [Google] [1]

Wiki page: [SceneJS Wiki page] [2]

Google group: [Google group] [3]

Google group "Brainstorming" discussion: [Google group discussion] [4]

PyCollada home: [PyCollada] [5]

PyCollada: [PyCollada on GitHub] [6]

  [1]: https://github.com/xeolabs/scenejs-pycollada        "GitHub project"
  [2]: http://scenejs.wikispaces.com/scenejs-pycollada  "SceneJS Wiki page"
  [3]: http://groups.google.com/group/scenejs    "Google group"
  [4]: http://groups.google.com/forum/#!topic/scenejs/jdNGC6oOA10 "New Collada translator (brainstorming)"
  [5]: http://collada.in4lines.com/    "PyCollada"
  [6]: https://github.com/pycollada/pycollada    "PyCollada on GitHub"

