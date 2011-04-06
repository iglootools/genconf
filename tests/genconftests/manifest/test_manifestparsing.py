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
from genconf.manifest import ManifestParser
from pkg_resources import resource_string

SIMPLE_MANIFEST = resource_string('genconftests', 'simple.yaml') 
NUMBER_OF_AUTO_GENERATED_PROPERTIES = 1
    
class ManifestParsingTestCase(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.parser = ManifestParser()
        self.manifest = self.parser.parse(SIMPLE_MANIFEST)
        
    def test_should_parse_simple_manifest(self): 
        assert len(self.manifest.profiles) == 2
    
    def test_should_create_development_profile(self): 
        development_profile = self.manifest.profile("development")
        assert development_profile.is_abstract == False
        assert len(development_profile.properties) == 3 + NUMBER_OF_AUTO_GENERATED_PROPERTIES
        assert len(development_profile._extends) == 1
        assert development_profile._extends[0] == self.manifest.profile("all")
        assert len(development_profile.output_files) == 3
        
    def test_should_create_all_profile(self): 
        all_profile = self.manifest.profile("all")
        assert all_profile.is_abstract == True
        assert len(all_profile.properties) == 2 + NUMBER_OF_AUTO_GENERATED_PROPERTIES
        assert len(all_profile._extends) == 0
    
    def test_should_override_properties(self):
        profile = self.manifest.profile("development")
        assert profile.properties['web.infrastructure.database.url'] == 'jdbc:postgresql://localhost/igloofinder_dev'
        
    def test_should_inherit_properties(self):
        profile = self.manifest.profile("development")
        assert len(profile.properties) == 3 + NUMBER_OF_AUTO_GENERATED_PROPERTIES
        assert profile.properties['dblogin'] == 'igloofinder'
        
    def test_should_inherit_outputfiles(self):
        profile = self.manifest.profile("development")
        assert len(profile.output_files) == 3
        
    def test_should_generate_filenames_based_on_given_profile(self):
        profile = self.manifest.profile("development")
        assert set([file.target_path for file in profile.output_files]) == set(["target/development/jdbc.properties", "target/development/web.xml", "target/anything"])

    def test_properties_should_contain_automatic_entries(self):
        dev = self.manifest.profile("development")
        assert dev.properties['profile'] == 'development'
        
        all = self.manifest.profile("all")
        assert all.properties["profile"] == "all"
    
    
    

