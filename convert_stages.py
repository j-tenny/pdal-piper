import os
import shutil

rst_files = [file for file in os.listdir('pdal/doc/stages') if file[-3:]=='.md']

lines = []
lines.append("class _GenericStage:\n")
lines.append("  def __init__(self,name, **kwargs):\n")
lines.append("      if 'classification' in kwargs.keys():\n")
lines.append("          kwargs['class'] = kwargs['classification']\n")
lines.append("          del (kwargs['classification'])\n")
lines.append("      self.name = name\n")
lines.append("      self.args = tuple(kwargs.items())\n")
lines.append("      self.args = tuple([arg for arg in self.args if (arg[1] is not None)])\n\n")

for file in rst_files:
    # Parse file
    with open('pdal/doc/stages/' + file, encoding="utf8") as f:
        doc_lines = f.readlines()
    doc_lines = [line.replace('\\','/') for line in doc_lines]

    # Get options
    options = []
    line_prev = doc_lines[0]
    line = doc_lines[1]
    i = 2
    while (i < len(doc_lines)):
        line_prev = doc_lines[i-1]
        line = doc_lines[i]
        if ("Options" in line_prev[0:10]) & ("------" in line):
            break
        i += 1
    if i < len(doc_lines):
        i += 1
        line = doc_lines[i]
    while (i<len(doc_lines)) and (line[0:5] != '-----') and (line[0:10]!='.. include') and (line[0:27]!='.. _assignment expressions:'):
        line = doc_lines[i]
        if line[0].isalpha() or (line[0:2]=='_`'):
            option = ''.join([char for char in line.split()[0] if char.isalnum() or char=='_'])
            option = option.lstrip('_')
            if (option == 'class'):
                option = 'classification'
            if (option == 'None') or (option == 'global'):
                pass
            else:
                options.append(option)
        i += 1

    # Add 'inputs' and 'tag' which are generic options for all stages?
    options.extend(['inputs','tag'])
    # Reformat for python script
    options_dict_str = '{' + ','.join(["'" + option + "':" + option for option in options]) + '}'

    if len(options)>0:
        options = ' = None, '.join(options) + ' = None,'
    else:
        options = ''


    # Create class definition
    lines.append("class " + file[:-3].replace('.','_') + "(_GenericStage):\n")
    lines.append("    \"\"\"\n")
    lines.extend(doc_lines)
    lines.append("\"\"\"\n")
    lines.append("\n")
    lines.append(f"    def __init__(self, {options} **kwargs):\n")
    lines.append(f"        args = " + options_dict_str + "\n")
    lines.append(f"        args.update(kwargs)\n")
    lines.append(f"        super().__init__('{file[:-3]}', **args)\n \n")


if os.path.exists('pdal_piper/stages.py'):
    os.remove('pdal_piper/stages.py')

with open('pdal_piper/stages.py','w', encoding="utf8") as f:
    f.writelines(lines)

shutil.copy2('usgs-lidar/boundaries/resources.geojson','pdal_piper/data/usgs_3dep_resources.geojson')