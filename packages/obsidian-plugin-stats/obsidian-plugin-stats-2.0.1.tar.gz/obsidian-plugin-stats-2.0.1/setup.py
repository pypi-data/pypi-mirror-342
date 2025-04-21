import setuptools
import distutils.core

setuptools.setup(
    name='obsidian-plugin-stats',
    version="2.0.1",
    author='@readwithai',
    long_description_content_type='text/markdown',
    author_email='talwrii@gmail.com',
    description='Fetch and maintain download statistics for an Obsidian Plugin',
    license='BSD',
    url='https://github.com/talwrii/obsidian-plugin-stats',
    packages=["obsidian_plugin_stats"],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['obsidian-plugin-stats=obsidian_plugin_stats.main:main']},
)
