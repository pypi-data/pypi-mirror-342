import os
import subprocess
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

from quote_module import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

class CMakeBuild(build_ext):
    def run(self):
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        source_dir = os.path.abspath(os.path.dirname(__file__))
        print(f"build_temp: {self.build_temp}")
        print(f"Source dir: {source_dir}")
        subprocess.check_call(['cmake', source_dir, '-DCMAKE_BUILD_TYPE=Release'], cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.', '--verbose'], cwd=self.build_temp)
        os.makedirs(self.build_lib, exist_ok=True)
        for ext in self.extensions:
            src_path = os.path.join(self.build_temp, 'quote_module', f'{ext.name}.so')
            dest_path = os.path.join(self.build_lib, 'quote_module', f'{ext.name}.so')
            print(f'\033[1;33mCopy {src_path} -> {dest_path} {ext.name}\033[0m')
            self.copy_file(src_path, dest_path)

    def build_extension(self, ext):
        pass

class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.universal = False

setup(
    name='quote_module',
    version=__version__,
    url='https://github.com/williamchen180/quote_module',
    author='William Chen',
    author_email='williamchen180@gmail.com',
    description='Your package description',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'setuptools',
        'wheel',
        'twine'
    ],
    ext_modules=[Extension('libquote_module', sources=[])],
    cmdclass={
        'build_ext': CMakeBuild,
        'bdist_wheel': bdist_wheel,
    },
    platforms=['linux_x86_64'],
)
