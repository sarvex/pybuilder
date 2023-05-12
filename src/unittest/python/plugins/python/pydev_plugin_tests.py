#   -*- coding: utf-8 -*-
#
#   This file is part of PyBuilder
#
#   Copyright 2011-2015 PyBuilder Team
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

try:
    TYPE_FILE = file
except NameError:
    from io import FileIO as TYPE_FILE


import unittest
from mock import patch, Mock, MagicMock, call

from pybuilder.core import Project
from pybuilder.plugins.python.pydev_plugin import (
    pydev_generate,
    init_pydev_plugin
)


class PydevPluginTests(unittest.TestCase):

    @patch('pybuilder.plugins.python.pydev_plugin.open', create=True)
    @patch('pybuilder.plugins.python.pydev_plugin.os')
    def test_should_write_pydev_files(self, os, mock_open):
        project = Project('basedir', name='pybuilder')
        project.set_property('dir_source_main_python', 'src/main/python')
        init_pydev_plugin(project)
        mock_open.return_value = MagicMock(spec=TYPE_FILE)
        os.path.join.side_effect = lambda first, second: f'{first}/{second}'

        pydev_generate(project, Mock())

        self.assertEqual(mock_open.call_args_list,
                         [call('basedir/.project', 'w'), call('basedir/.pydevproject', 'w')])
        metadata_file = mock_open.return_value.__enter__.return_value

        self.assertEqual(metadata_file.write.call_args_list,
                         [call("""<?xml version="1.0" encoding="UTF-8"?>

<!-- This file has been generated by the PyBuilder Pydev Plugin -->

<projectDescription>
    <name>pybuilder</name>
    <comment></comment>
    <projects>
    </projects>
    <buildSpec>
        <buildCommand>
            <name>org.python.pydev.PyDevBuilder</name>
            <arguments>
            </arguments>
        </buildCommand>
    </buildSpec>
    <natures>
        <nature>org.python.pydev.pythonNature</nature>
    </natures>
</projectDescription>
"""),
                          call("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?eclipse-pydev version="1.0"?>

<!-- This file has been generated by the PyBuilder Pydev Plugin -->

<pydev_project>
    <pydev_property name="org.python.pydev.PYTHON_PROJECT_INTERPRETER">Default</pydev_property>
    <pydev_property name="org.python.pydev.PYTHON_PROJECT_VERSION">python 2.7</pydev_property>
    <pydev_pathproperty name="org.python.pydev.PROJECT_SOURCE_PATH">
\t\t<path>/pybuilder/src/main/python</path>

    </pydev_pathproperty>
</pydev_project>
""")])
