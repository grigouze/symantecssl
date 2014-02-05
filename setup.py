try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


def read(relative):
    contents = open(relative, 'r').read()
    return [l for l in contents.split('\n') if l != '']


setup(
    name='symantecssl',
    version=read('VERSION')[0],
    description='Supports working with the Symantec SSL service',
    author='Rackspace Barbican Team',
    author_email='',
    tests_require=read('test-requirements.txt'),
    install_requires=read('requirements.txt'),
    test_suite='nose.collector',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup', 'tests'])
)
