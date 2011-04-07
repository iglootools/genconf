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
from genconf.manifest import TemplateNotFoundException, TemplateProcessingException

class DefaultFileEventListener(object):
    def on_before_profile(self, profile):
        pass
    def on_after_profile(self, profile):
        pass
    def on_before_file_update(self, filename, content):
        pass
    def on_after_file_update(self, filename, content):
        pass
    def on_template_not_found(self, template_not_found_exception):
        pass
    def on_template_processing_error(self, template_processing_exception):
        pass
    def on_write_error(self, target_path, ex):
        pass

class FileGenerator(object):
    def __init__(self, template_loader, targetdir):
        assert template_loader is not None, "template_loader is required"
        assert targetdir is not None, "targetdir is required"
        self._template_loader = template_loader
        self._targetdir = targetdir
        
    
    def generate_files(self, manifest, file_event_listener=DefaultFileEventListener()):
        profiles = manifest.concrete_profiles()
        for p in profiles:
            file_event_listener.on_before_profile(p)
            for f in p.output_files:
                filename = os.path.join(self._targetdir, f.target_path)
                file_event_listener.on_before_file_update(filename)
                try:                    
                    directory = os.path.dirname(filename)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    content = f.render(self._template_loader)
                    with codecs.open(filename, "wb", encoding="utf-8") as f:
                        f.write(content)
                    file_event_listener.on_after_file_update(filename, content)
                except TemplateNotFoundException as e:
                    file_event_listener.on_template_not_found(e)
                except TemplateProcessingException as e:
                    file_event_listener.on_template_processing_error(e)
                except Exception as e:
                    file_event_listener.on_write_error(filename, e)
            file_event_listener.on_after_profile(p)