from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        self.execute(self._post_install, [], msg="Running post install task")

    def _post_install(self):
        try:
            from pdal_piper.skeletons import generate_skeletons
            generate_skeletons()
        except ImportError as e:
            print(f"Warning: Could not import generate_skeletons: {e}")
        except Exception as e:
            print(f"Warning: Failed to generate pipeline.pyi: {e}")

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        self.execute(self._post_install, [], msg="Running post develop task")

    def _post_install(self):
        try:
            from pdal_piper.skeletons import generate_skeletons
            generate_skeletons()
        except ImportError as e:
            print(f"Warning: Could not import generate_skeletons: {e}")
        except Exception as e:
            print(f"Warning: Failed to generate pipeline.py: {e}")

setup(
    name='pdal-piper',
    version='0.2.1',
    packages=['pdal_piper'],
    url='https://github.com/j-tenny/pdal-piper',
    license='MIT',
    author='Johnathan Tenny (j-tenny)',
    author_email='jt893@nau.edu',
    description='Type stubs and utilities for PDAL (Point Data Abstraction Library) and USGS 3DEP lidar download.',
    cmdclass = {
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
    },
)

