from setuptools import setup
# from distutils.core import setup

setup(
    name='application',
    version='0.1',
    description="Gui Packages",
    author="Eric Misfeld",
    author_email="mier1011@h-ka.de",
    packages=['app', 'controller', 'view', 'model', 'styles']
    # package_dir = {'': 'src'}
)
