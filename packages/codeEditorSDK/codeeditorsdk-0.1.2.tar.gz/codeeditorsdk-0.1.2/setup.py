from setuptools import setup, find_packages

setup(
    name='codeEditorSDK',
    version='0.1.2',
    description='Multi-language code editor SDK with Tree-sitter support',
    author='Ziyang',
    author_email='zyang253@ucr.edu',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'tree_sitter==0.20.1',
        'tree_sitter_languages>=1.5.0',
    ],
    python_requires='>=3.7, <=3.11',

)