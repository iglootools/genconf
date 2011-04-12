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
from genconf.manifest import ManifestOverridesParser
from tests.genconftests import samples
    
class ManifestOverridesParsingTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.parser = ManifestOverridesParser()
        self.overrides = self.parser.parse(samples.simple_overrides_stream)
        
    def test_should_parse_simple_overrides(self):
        assert self.overrides == {
            'simple': {
               'all': {
                   'dblogin': 'login-all-override'
               },
               'development': {
                   'web_infrastructure_database_url': 'jdbc://development-override'
               }
           }
        }
    
   
    