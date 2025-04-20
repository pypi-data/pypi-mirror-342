from setuptools import setup

def post_install():
    import subprocess
    import sys
    import os
    import shutil
    print("Building Zig library...")
    subprocess.check_call([sys.executable, '-m', 'ziglang', 'build', 'lib'])
    import tokenizerz
    package_dir = os.path.dirname(os.path.abspath(tokenizerz.__file__))
    source_dir = os.path.abspath('zig-out')
    target_dir = os.path.join(package_dir, 'zig-out')
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir)

setup(
    name="tokenizerz",
    version="0.0.1a6",
    author="J Joe",
    author_email="backupjjoe@gmail.com",
    description="Minimal BPE tokenizer in Zig",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaco-bro/tokenizer",
    py_modules=['tokenizerz'],
    python_requires=">=3.12.8",
    install_requires=['ziglang==0.13.0.post1'],
    data_files=[
        ('', ['build.zig', 'build.zig.zon']),
        ('src', ['src/tokenizer.zig']),
    ],
    entry_points={
        "console_scripts": ["bpe=tokenizerz:demo"],
        "distutils.post_install": ["post_install=setup:post_install"],
    },
    zip_safe=False,
)
