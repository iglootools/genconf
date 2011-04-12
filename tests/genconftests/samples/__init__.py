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
from pkg_resources import resource_string
from genconf.manifest import ManifestParser, ManifestOverridesParser

simple_manifest_stream = resource_string('tests.genconftests.samples', 'simple.yaml')
simple_manifest = ManifestParser().parse(simple_manifest_stream)
development_profile = simple_manifest.profile("development")
all_profile = simple_manifest.profile("all")

simple_overrides_stream = resource_string('tests.genconftests.samples', 'simple-overrides.yaml')
simple_overrides = ManifestOverridesParser().parse(simple_overrides_stream)