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
import codecs
class FileGenerator(object):
    def __init__(self, template_loader, targetdir):
        assert template_loader is not None, "template_loader is required"
        assert targetdir is not None, "targetdir is required"
        self._template_loader = template_loader
        self._targetdir = targetdir
        
    
    def generate_files(self, manifest):
        profiles = manifest.concrete_profiles()
        for p in profiles:
            for f in p.output_files:
                filename = os.path.join(self._targetdir, f.target_path)
                directory = os.path.dirname(filename)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                content = f.render(self._template_loader)
                with codecs.open(filename, "wb", encoding="utf-8") as f:
                    f.write(content)