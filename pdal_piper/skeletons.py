from pdal import libpdalpython

PDAL_VERSION = getattr(libpdalpython.getInfo(),'version')

def tab(n_tabs, n_spaces = 4):
    return ' ' * n_tabs * n_spaces

class class_skeleton:
    def __init__(self,class_name):
        self.class_name = class_name
        self.methods = []

    def add_method(self, name, description, options):
        self.methods.append(class_method_skeleton(name, description, options))

    def to_string(self):
        s = f"class {self.class_name}:\n"
        for method in self.methods:
            s += method.to_string() + "\n"
        return s


class class_method_skeleton:
    def __init__(self, name, description, options):
        self.fullname = name
        self.name = name.split('.')[1]
        self.description = description
        self.options = options

    @property
    def option_names(self):
        return [option['name'] for option in self.options]


    @property
    def arg_string(self):
        args_list = []
        for option in self.options:
            if 'default' in option:
                default = option['default']
                if type(default) is str:
                    if default.isnumeric():
                        option_str = f'{option["name"]} = {default}'
                    else:
                        option_str = f'{option["name"]} = {repr(default)}'
                else:
                    raise TypeError(f"Can not interpret default {default} of {option['name']}")

            else:
                option_str = f'{option["name"]} = None'
            args_list.append(option_str)

        args = ', '.join(args_list)

        return f"{tab(1)}def {self.name}(self,{args}):\n"

    @property
    def docstring(self):
        s = f"{tab(2)}\"\"\"{self.description}\n\n"
        s += f'Documentation represents PDAL version {PDAL_VERSION}\n\n'
        s += f'https://pdal.io/en/{PDAL_VERSION}/stages/{self.fullname}.html\n\n'
        s += f"{tab(2)}Options:\n"
        for option in self.options:
            s += f"{tab(3)}{option['name']}: {option['description']}\n"
        s += f"{tab(2)}\"\"\"\n\n"
        return s

    def to_string(self):
        return self.arg_string + self.docstring

def generate_skeletons():
    from pdal import pipeline
    from pathlib import Path

    pipeline_py_path = Path(pipeline.__file__)
    pipeline_pyi_path = pipeline_py_path.parent / (pipeline_py_path.stem + '.pyi')

    reader_sk = class_skeleton('Reader')
    filter_sk = class_skeleton('Filter')
    writer_sk = class_skeleton('Writer')

    drivers = libpdalpython.getDrivers()
    options = libpdalpython.getOptions()

    for driver in drivers:
        driver_name = driver["name"]
        driver_name_rhs = driver_name.split(".")[1]
        description = driver["description"]
        driver_options = options[driver_name]

        # Move the boring options to the end
        indexes_move = [i for i in range(len(driver_options))
                        if driver_options[i]['name'] in ['user_data','log','option_file','where','where_merge']]
        indexes_move.reverse()
        for i in indexes_move:
            driver_options.append(driver_options.pop(i))


        driver_options.extend([{'name':'inputs','description':''},{'name':'tag','description':''}])

        if driver_name.split('.')[0]=='readers':
            reader_sk.add_method(driver_name, description, driver_options)
        elif driver_name.split('.')[0]=='filters':
            filter_sk.add_method(driver_name, description, driver_options)
        elif driver_name.split('.')[0]=='writers':
            writer_sk.add_method(driver_name, description, driver_options)

    with open(pipeline_pyi_path,'w') as f:
        # Copy code from pipeline.py
        with open(pipeline_py_path) as template:
            lines = []
            line = template.readline()
            pipeline = False
            while line:
                # Define stub for arrays property
                if 'class Pipeline' in line:
                    pipeline = True
                if pipeline and '@property' in line:
                    lines.append(tab(1)+'@property\n')
                    lines.append(tab(1)+"def arrays(self) -> 'np.ndarray':\n")
                    lines.append(tab(2)+"return self.arrays\n\n")
                    pipeline = False

                # Skip lines where Filter, Reader, and Writer are defined
                if ('class Filter' in line) or ('class Reader' in line) or ('class Writer' in line):
                    line = template.readline()
                    while line and line.lstrip() != line:
                        line = template.readline()

                else:
                    lines.append(line)
                    line = template.readline()

        new_text = ''.join(lines) + reader_sk.to_string() + filter_sk.to_string() + writer_sk.to_string()

        f.write(new_text)