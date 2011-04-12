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
from genconf.manifest._profile import NUMBER_OF_AUTO_GENERATED_PROPERTIES, Profile
from tests.genconftests.samples import development_profile, all_profile 

class ProfileTestCase(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        
    def test_should_override_properties(self):
        profile = Profile('development', 
            properties={
                'web_infrastructure_database_url': 'jdbc:postgresql://localhost/igloofinder_dev',
                'web_infrastructure_database_login': 'dev_db_login'
            }, 
            overrides={
                'web_infrastructure_database_login': 'my-login-override'
           })
        
        assert profile.properties['web_infrastructure_database_login'] == 'my-login-override'
        
    def test_should_inherit_properties(self):
        assert len(development_profile.properties) == 3 + NUMBER_OF_AUTO_GENERATED_PROPERTIES
        assert development_profile.properties['dblogin'] == 'igloofinder'
        
    def test_should_inherit_outputfiles(self):
        assert len(development_profile.output_files) == 3
        
    def test_should_generate_filenames_based_on_given_profile(self):
        assert set([file.target_path for file in development_profile.output_files]) == set(["target/development/jdbc.properties", "target/development/some.xml", "target/sometext"])

    def test_properties_should_contain_automatic_entries(self):
        assert development_profile.properties['profile'] == 'development'
        assert all_profile.properties["profile"] == "all"
        assert development_profile.properties['truefalse'](True) == 'true'
        assert development_profile.properties['truefalse'](False) == 'false'
        assert development_profile.properties['either'](True, 'val1', 'val2') == 'val1'
        assert development_profile.properties['either'](False, 'val1', 'val2') == 'val2'
