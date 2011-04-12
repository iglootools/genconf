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
import os
from genshi.template import TemplateLoader, loader
from genconf.manifest import ManifestParser, ManifestParsingError, ManifestOverridesParser, ManifestOverridesParsingError
from genconf.filegenerator import FileGenerator, DefaultEventListener, DefaultErrorListener

class DefaultGenConfEventListener(DefaultEventListener):
    def on_manifest_parsed(self, manifest_path, manifest):
        pass
    def on_overrides_parsed(self, overrides_path, overrides):
        pass
    def on_overrides_ignored(self, overrides_path):
        pass                   

class DefaultGenConfErrorListener(object):
    def on_manifest_parsing_error(self, manifest_path, manifest_parsing_error):
        raise Exception, str(manifest_parsing_error), sys.exc_info()[2]
    def on_overrides_parsing_error(self, overrides_path, overrides_parsing_error):
        raise Exception, str(overrides_parsing_error), sys.exc_info()[2]
    def on_template_not_found(self, template_not_found_exception):
        raise Exception, str(template_not_found_exception), sys.exc_info()[2]
    def on_template_processing_error(self, template_processing_exception):
        raise Exception, str(template_processing_exception), sys.exc_info()[2]
    def on_write_error(self, target_path, ex):
        raise Exception, str(ex), sys.exc_info()[2]
        

class GenConf(object):
    def __init__(self, manifest_path, overrides_path, templatedir, targetdir, ):
        self._manifest_path = manifest_path
        self._overrides_path = overrides_path
        self._template_loader = TemplateLoader([templatedir])
        self._file_generator = FileGenerator(self._template_loader, targetdir)
        self._manifest_parser = ManifestParser()
        self._overrides_parser = ManifestOverridesParser()
        
    
    def generate(self, error_listener=DefaultGenConfErrorListener(), event_listener=DefaultGenConfEventListener()):
        overrides = self._parse_overrides(error_listener, event_listener)
        
        with codecs.open(self._manifest_path, 'rb', 'utf-8') as f:
            try:
                manifest = self._manifest_parser.parse(f, overrides)
                event_listener.on_manifest_parsed(self._manifest_path, manifest)
                self._file_generator.generate_files(manifest, error_listener, event_listener)
            except ManifestParsingError, e:
                error_listener.on_manifest_parsing_error(self._manifest_path, e)
    
    def _parse_overrides(self, error_listener, event_listener):
        if os.path.exists(self._overrides_path):
            with codecs.open(self._overrides_path, 'rb', 'utf-8') as f:
                try:
                    overrides = self._overrides_parser.parse(f)
                    event_listener.on_overrides_parsed(self._overrides_path, overrides)
                    return overrides
                except ManifestOverridesParsingError, e: 
                    error_listener.on_overrides_parsing_error(self._overrides_path, e)
        else:
            event_listener.on_overrides_ignored(self._overrides_path)
            return {}