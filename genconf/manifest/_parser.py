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

import yaml
from genconf.manifest._manifest import Manifest
from genconf.manifest._profile import Profile
from genconf.manifest._outputfile import OutputFile

class ManifestParser(object):
    def __init__(self):
        pass
    
    def parse(self, stream):
        """ Parse a stream and returns a Manifest object"""
        doc = yaml.load(stream)
        
        created_profiles = dict()
        
        def create_output_file(profile_provider):
            def f(data):
                return OutputFile(profile_provider, 
                                  target_path = data['target'],
                                  template_path = data['template'],
                                  template_format = data['template_format'])
            return f
        def create_profile(data):
            return get_profile(data['name'])
        
        def get_profile(name):
            if name in created_profiles:
                return created_profiles[name]
            else:
                return do_create_profile(next((p for p in doc['profiles'] if p['name'] == name), None))
                
        def do_create_profile(data):
            p = Profile(name = data['name'], 
                           is_abstract = data['abstract'],
                           extends = map(get_profile, data['extends']),
                           properties = data['properties'],
                           output_files = map(create_output_file(lambda: p), data['output_files']))
            created_profiles[p.name] = p
            return p
        
        return Manifest(map(create_profile, doc['profiles']))