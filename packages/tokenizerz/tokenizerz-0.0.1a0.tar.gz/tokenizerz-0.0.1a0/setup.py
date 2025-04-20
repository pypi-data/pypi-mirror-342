import os
import sys
import subprocess
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.build_ext import build_ext

class PipZig(build_ext):
    def run(self):
        super().run()
        build_lib()

class DevZig(develop):
    def run(self):
        super().run()
        build_lib()

def build_lib():
    subprocess.check_call([ sys.executable, '-m', 'ziglang', 'build', 'lib' ])
    print(f"Zig library built in: {os.path.abspath('zig-out/lib')}")

setup(
    name="tokenizerz",
    version="0.0.1a0",
    author="J Joe",
    author_email="backupjjoe@gmail.com",
    description="Minimal BPE tokenizer in Zig",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaco-bro/tokenizer",
    py_modules=['tokenizerz'],
    python_requires=">=3.12.8",
    install_requires=['ziglang==0.13.0.post1'],
    entry_points={ "console_scripts": [ "bpe=tokenizerz:demo" ] },
    cmdclass={ 
        'develop': DevZig,
        'build_ext': PipZig,
    },
    data_files=[
        ('', ['build.zig', 'build.zig.zon']),
        ('src', ['src/tokenizer.zig']),
    ],
)

