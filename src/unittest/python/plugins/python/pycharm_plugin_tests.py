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
from mock import patch, Mock, MagicMock

from pybuilder.core import Project
from pybuilder.plugins.python.pycharm_plugin import (
    pycharm_generate,
    _ensure_directory_present
)


class PycharmPluginTests(unittest.TestCase):

    @patch('pybuilder.plugins.python.pycharm_plugin.os')
    def test_should_create_pycharm_directory_if_not_present(self, os):
        os.path.exists.return_value = False

        _ensure_directory_present('foo')

        os.makedirs.assert_called_with('foo')

    @patch('pybuilder.plugins.python.pycharm_plugin.os')
    def test_should_not_create_pycharm_directory_if_present(self, os):
        os.path.exists.return_value = True

        _ensure_directory_present('foo')

        self.assertFalse(os.makedirs.called)

    @patch('pybuilder.plugins.python.pycharm_plugin.open', create=True)
    @patch('pybuilder.plugins.python.pycharm_plugin.os')
    def test_should_write_pycharm_file(self, os, mock_open):
        project = Project('basedir', name='pybuilder')
        project.set_property('dir_source_main_python', 'src/main/python')
        mock_open.return_value = MagicMock(spec=TYPE_FILE)
        os.path.join.side_effect = lambda first, second: f'{first}/{second}'

        pycharm_generate(project, Mock())

        mock_open.assert_called_with('basedir/.idea/pybuilder.iml', 'w')
        metadata_file = mock_open.return_value.__enter__.return_value
        metadata_file.write.assert_called_with("""<?xml version="1.0" encoding="UTF-8"?>
<!-- This file has been generated by the PyBuilder PyCharm Plugin -->

<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$">
      <sourceFolder url="file://$MODULE_DIR$/src/main/python" isTestSource="false" />
      <excludeFolder url="file://$MODULE_DIR$/target" />
    </content>
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
  <component name="PyDocumentationSettings">
    <option name="myDocStringFormat" value="Plain" />
  </component>
  <component name="TestRunnerService">
    <option name="projectConfiguration" value="Unittests" />
    <option name="PROJECT_TEST_RUNNER" value="Unittests" />
  </component>
</module>
""")
