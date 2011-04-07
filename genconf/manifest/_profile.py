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
NUMBER_OF_AUTO_GENERATED_PROPERTIES = 1

class Profile(object):
    def __init__(self, name, is_abstract, extends, properties, output_files):
        assert name is not None, "name is required"
        assert is_abstract is not None, "is_abstract is required"
        assert extends is not None, "extends is required"
        assert properties is not None, "properties is required"
        assert output_files is not None, "output_files is required"
        self.name = name
        self.is_abstract = is_abstract
        self._extends = extends
        self._properties = properties
        self._output_files = output_files
        
    def get_properties(self):
        data = dict()
        for extended_profile in self._extends:
            data.update(extended_profile.properties)
        data.update(self._properties)
        data['profile'] = self.name
        return data
    
    def get_output_files(self):
        files = []
        for extended_profile in self._extends:
            files.extend(map(lambda of: of.with_profile(self), extended_profile.output_files))
        files.extend(self._output_files)
        return files
    
    properties = property(get_properties, None)
    output_files = property(get_output_files, None)
    
    def __eq__(self, other):
        return self.name == other.name
    