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
from genshi.template import TemplateLoader, loader
import codecs
from genconf.manifest import ManifestParser
from genconf.filegenerator import FileGenerator, DefaultFileEventListener

class DefaultGenConfEventListener(DefaultFileEventListener):
    def on_manifest_parsed(self, manifest_path, manifest):
        pass

class GenConf(object):
    def __init__(self, manifest_path, templatedir, targetdir, ):
        self._template_loader = TemplateLoader([templatedir])
        self._file_generator = FileGenerator(self._template_loader, targetdir)
        self._manifest_parser = ManifestParser()
        self._manifest_path = manifest_path
    
    def generate(self, event_listener=DefaultGenConfEventListener()):
        with codecs.open(self._manifest_path, 'rb', 'utf-8') as f:
            manifest = self._manifest_parser.parse(f)
            event_listener.on_manifest_parsed(self._manifest_path, manifest)
            self._file_generator.generate_files(manifest, event_listener)