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
import os
import tempfile
import unittest
from genconf import GenConf
from pkg_resources import resource_filename
    
class GenConfTestCase(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._tmpdirectory = tempfile.mkdtemp()
        self.genconf = GenConf(manifest_path=resource_filename('tests.genconftests.samples', 'simple.yaml'), 
                               templatedir=resource_filename('tests.genconftests.samples', 'templates'), 
                               targetdir=self._tmpdirectory)

        
    def test_should_generate_all_files(self): 
        self.genconf.generate()
        assert os.path.exists(os.path.join(self._tmpdirectory, 'target', 'development', 'jdbc.properties')) == True
        assert os.path.exists(os.path.join(self._tmpdirectory, 'target', 'development', 'some.xml')) == True
        assert os.path.exists(os.path.join(self._tmpdirectory, 'target', 'sometext')) == True
    
   
    
    

