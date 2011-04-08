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

import sys
import argparse
import os
import traceback
from genconf import GenConf, DefaultGenConfEventListener, DefaultGenConfErrorListener

class PrintProgressListener(DefaultGenConfEventListener):
    def on_manifest_parsed(self, manifest_path, manifest):
        print("Using Manifest [%s] and will generate files for %s:" %(manifest_path, [p.name for p in manifest.concrete_profiles()]))
    def on_before_file_update(self, filename):
        print("  Updating file: %s" % (filename,))
    def on_after_file_update(self, filename, content):
        pass
    def on_before_profile(self, profile):
        print("")
        print("Profile: %s" % (profile.name,))
    def on_after_profile(self, profile):
        print("... DONE")
        print("")
 
class PrintErrorListener(DefaultGenConfErrorListener):
    def __init__(self, templatedir):
        self._templatedir=templatedir
        self.exit = 0
        
    def on_template_not_found(self, template_not_found_exception):
        print >> sys.stderr, '    [ERROR] Template not found: %s (Looking for templates in: %s)' % (template_not_found_exception.path, self._templatedir)
        self._on_error()
    def on_template_processing_error(self, template_processing_exception):
        print >> sys.stderr, '    [ERROR] Error while processing template: %s. %s' % (template_processing_exception.path, str(template_processing_exception))
        #traceback.print_exc(template_processing_exception)
        self._on_error()
    def on_write_error(self, target_path, ex):
        print >> sys.stderr, '    [ERROR] Error while writing file: %s. Error: %s' % (target_path, str(ex))
        self._on_error() 
        
    def _on_error(self):
        self.exit = 1

def run():
    "run the command in sys.argv"
    sys.exit(dispatch(sys.argv[1:]))
    
def dispatch(argv):
    "run the command specified in args"
    args = parse_args(argv)
    print_settings(args)
    check_args(args)
    
    if(args.verbose):
        progress_listener = PrintProgressListener()
    else:
        progress_listener = DefaultGenConfEventListener()
        
    error_listener = PrintErrorListener(args.templatedir)
    
    
    genconf = GenConf(manifest_path=args.manifest, 
                               templatedir=args.templatedir, 
                               targetdir=args.targetdir)
    genconf.generate(error_listener, progress_listener)
    
    return error_listener.exit

def check_args(args):
    if not os.path.exists(args.manifest):
        print >> sys.stderr, '[ERROR] Manifest not found: %s)' % (args.manifest,)
        sys.exit(1)

def parse_args(argv):
    parser = argparse.ArgumentParser(prog="gc", description='Generate configuration files.')
    parser.add_argument('-m','--manifest', dest='manifest', action='store', 
                        default=os.path.join(os.curdir, 'genconf-manifest.yaml'),
                        help='the genconf-YAML manifest to use (default: ./genconf-manifest.yaml)')
    parser.add_argument('-t','--target-directory', dest='targetdir', action='store', 
                        default=os.curdir,
                        help='the target directory into which files will be generated (default: the current directory)')
    parser.add_argument('-T','--template-directory', dest='templatedir', action='store', 
                        default=os.curdir,
                        help='the directory in which the templates reside (default: the current directory)')
    parser.add_argument('-v','--verbose', dest='verbose', action='store_true', 
                        default=False,
                        help='Whether to print additional progress messages')
    args = parser.parse_args(argv)
    return args
def print_settings(args):
    if(args.verbose):
        print("""
      ____             ____             __ 
     / ___| ___ _ __  / ___|___  _ __  / _|
    | |  _ / _ \ '_ \| |   / _ \| '_ \| |_ 
    | |_| |  __/ | | | |__| (_) | | | |  _|
     \____|\___|_| |_|\____\___/|_| |_|_|  
                                               
        """)
        print("Settings: ")
        print(" - Manifest: %s" % os.path.abspath(args.manifest))
        print(" - Target Directory: %s" % os.path.abspath(args.targetdir))
        print(" - Template Directory: %s" % os.path.abspath(args.templatedir))
        print("")
    