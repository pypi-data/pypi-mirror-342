import os
import sys
import shutil
import subprocess
from setuptools import setup, Extension
from setuptools.command.develop import develop
from setuptools.command.build_ext import build_ext

dummy_ext = Extension('_tokenizerz_dummy', sources=[])

class PipZig(build_ext):
    def run(self):
        subprocess.check_call([sys.executable, '-m', 'ziglang', 'build', 'lib'])
        source_dir = os.path.abspath('zig-out')
        target_dir = os.path.join(self.build_lib, 'zig-out')
        print('PipZig:', source_dir, target_dir)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)

class DevZig(develop):
    def run(self):
        super().run()
        subprocess.check_call([sys.executable, '-m', 'ziglang', 'build', 'lib'])

setup(
    name="tokenizerz",
    version="0.0.1a4",
    author="J Joe",
    author_email="backupjjoe@gmail.com",
    description="Minimal BPE tokenizer in Zig",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaco-bro/tokenizer",
    py_modules=['tokenizerz'],
    python_requires=">=3.12.8",
    install_requires=['ziglang==0.13.0.post1'],
    ext_modules=[dummy_ext],
    entry_points={ "console_scripts": [ "bpe=tokenizerz:demo" ] },
    cmdclass={ 
        'develop': DevZig,
        'build_ext': PipZig,
    },
    data_files=[
        ('', ['build.zig', 'build.zig.zon']),
        ('src', ['src/tokenizer.zig']),
    ],
    zip_safe=False,
)
