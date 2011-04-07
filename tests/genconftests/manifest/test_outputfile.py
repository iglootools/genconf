"""
   Copyright 2011 Sami Dalouche

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import unittest
from tests.genconftests.samples import development_profile, all_profile
from genshi.template import TemplateLoader, loader 
from pkg_resources import resource_filename

class OutputFileTestCase(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._templatedir = resource_filename('tests.genconftests.samples', 'templates')
        self._template_loader = TemplateLoader([self._templatedir])
    
    def test_should_render_text_template(self):
        expected = """Current profile: development. Database: jdbc:postgresql://localhost/igloofinder_dev"""
        output_file = [file for file in development_profile.output_files if file.target_path == "target/sometext"][0]
        assert output_file.render(self._template_loader) == expected

    def test_should_render_xml_template(self):
        expected = """<?xml version="1.0" encoding="UTF-8"?>
<myxml>Current profile: development. Database: jdbc:postgresql://localhost/igloofinder_dev</myxml>"""
        output_file = [file for file in development_profile.output_files if file.target_path == "target/development/some.xml"][0]
        
        assert output_file.render(self._template_loader) == expected