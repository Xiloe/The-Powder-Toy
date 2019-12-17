import hashlib
import os
import re

source_root = os.environ['GENERATE_VS_FILTERS_SOURCE_ROOT']
build_root = os.environ['GENERATE_VS_FILTERS_BUILD_ROOT']
project_name = os.environ['GENERATE_VS_FILTERS_PROJECT_NAME']

counter = 0
paths_to_ids = {}
files_to_parents = {}
while True:
	key = 'GENERATE_VS_FILTERS_{0}'.format(counter)
	counter += 1
	if key not in os.environ:
		break
	file = os.environ[key]
	if not file.startswith('src\\') and not file.startswith('data\\'):
		continue
	parent = re.match(r'(.+)\\[^\\]+', file)[1]
	if parent not in paths_to_ids:
		digest = hashlib.sha256(file.encode('utf-8')).hexdigest()
		paths_to_ids[parent] = '{{{0}-{1}-{2}-{3}-{4}}}'.format(digest[0 : 8], digest[8 : 12], digest[12 : 16], digest[16 : 20], digest[20 : 32])
	files_to_parents['{0}\\{1}'.format(source_root, file)] = parent

with open('{0}\\{1}.vcxproj.filters'.format(build_root, project_name), 'w') as filters:
	filters.write(r"""<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup>
""")
	for path in paths_to_ids:
		filters.write(r"""    <Filter Include="{0}">
      <UniqueIdentifier>{1}</UniqueIdentifier>
    </Filter>
""".format(path, paths_to_ids[path]))
	filters.write(r"""  </ItemGroup>
  <ItemGroup>
""")
	for file in files_to_parents:
		filters.write(r"""    <ClCompile Include="{0}">
      <Filter>{1}</Filter>
    </ClCompile>
""".format(file, files_to_parents[file]))
	filters.write(r"""  </ItemGroup>
</Project>
""")
