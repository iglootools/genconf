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
import codecs
import sys
from genshi.template import TemplateLoader, loader
from genconf.manifest import ManifestParser
from genconf.filegenerator import FileGenerator, DefaultEventListener, DefaultErrorListener

class DefaultGenConfEventListener(DefaultEventListener):
    def on_manifest_parsed(self, manifest_path, manifest):
        pass

class DefaultGenConfErrorListener(object):
        
    def on_template_not_found(self, template_not_found_exception):
        raise Exception, str(template_not_found_exception), sys.exc_info()[2]
    def on_template_processing_error(self, template_processing_exception):
        raise Exception, str(template_processing_exception), sys.exc_info()[2]
    def on_write_error(self, target_path, ex):
        raise Exception, str(ex), sys.exc_info()[2]
        

class GenConf(object):
    def __init__(self, manifest_path, templatedir, targetdir, ):
        self._template_loader = TemplateLoader([templatedir])
        self._file_generator = FileGenerator(self._template_loader, targetdir)
        self._manifest_parser = ManifestParser()
        self._manifest_path = manifest_path
    
    def generate(self, error_listener=DefaultGenConfErrorListener(), event_listener=DefaultGenConfEventListener()):
        with codecs.open(self._manifest_path, 'rb', 'utf-8') as f:
            manifest = self._manifest_parser.parse(f)
            event_listener.on_manifest_parsed(self._manifest_path, manifest)
            self._file_generator.generate_files(manifest, error_listener, event_listener)