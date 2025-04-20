from setuptools import setup, find_packages

setup(
    name='terminal_text_style',
    version='0.0.1',
    description='Style texts in the terminal with colors, backgrounds and styles in an easy way.',
    long_description_content_type= 'text/markdown',
    author='Victor Paiva',
    author_email='victor_eduardof@hotmail.com',
    url= 'https://github.com/Victor-f-Paiva/terminal-text-style.git',
    packages=find_packages(),
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='terminal style color ansi cli',
)
