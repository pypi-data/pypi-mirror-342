# setup.py
import os
import sys
import shutil
import subprocess
from setuptools import setup
from setuptools.command.install import install

class InstallWithZigBuild(install):
    def run(self):
        super().run()
        print("Building Zig library...")
        subprocess.check_call([sys.executable, '-m', 'ziglang', 'build', 'lib'])
        source_dir = os.path.abspath('zig-out')
        target_dir = os.path.join(self.install_lib, 'zig-out')
        print(f"Copying from {source_dir} to {target_dir}")
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)

setup(
    name="tokenizerz",
    version="0.0.1a5",
    author="J Joe",
    author_email="backupjjoe@gmail.com",
    description="Minimal BPE tokenizer in Zig",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaco-bro/tokenizer",
    py_modules=['tokenizerz'],
    python_requires=">=3.12.8",
    install_requires=['ziglang==0.13.0.post1'],
    cmdclass={'install': InstallWithZigBuild},
    data_files=[
        ('', ['build.zig', 'build.zig.zon']),
        ('src', ['src/tokenizer.zig']),
    ],
    entry_points={"console_scripts": ["bpe=tokenizerz:demo"]},
    zip_safe=False,
)
