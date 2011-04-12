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
import sys

class ManifestParsingError(Exception):
    pass

class ManifestParser(object):
    def __init__(self):
        pass
    
    def parse(self, stream, overrides={}):
        """ Parse a stream and returns a Manifest object"""
        try:
            doc = yaml.load(stream)
        except Exception, e:
            raise ManifestParsingError, str(e), sys.exc_info()[2]
        
        project_overrides = overrides.get(doc['project'], {})
        
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
                           output_files = map(create_output_file(lambda: p), data['output_files']),
                           overrides = project_overrides.get(data['name'], {}))
            created_profiles[p.name] = p
            return p
        
        return Manifest(doc['project'], map(create_profile, doc['profiles']))
    
class ManifestOverridesParsingError(Exception):
    pass

class ManifestOverridesParser(Exception):
    def parse(self, stream):
        """ Parse a stream and returns a dict[project,dict[profile, properties]]"""
        try:
            doc = yaml.load(stream)
        except Exception, e:
            raise ManifestOverridesParsingError, str(e), sys.exc_info()[2]
        
        overrides = dict()
        for project, profile in doc.items():
            project_profiles = dict()
            for k,v in profile.items():
                project_profiles[k] = v
                
            overrides[project] = project_profiles
        return overrides