import os

from setuptools import setup, find_packages

with open(os.path.join('ailive', '__version__.py')) as version_file:
    exec(version_file.read())

# read from requirements.txt
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()


setup(
    name='ailive',
    author='Roei Bar Aviv',
    author_email='roei@springsoftware.io',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
    ],
    description='Misc. pure-python utilities',
    license='LICENSE.txt',
    version=__version__,
    packages=find_packages(),
    namespace_packages=['ailive'],
    install_requires=install_requires,
    zip_safe=False,
    scripts=[],
    long_description=open('README.md').read(),
    entry_points=dict(
        console_scripts=[
            'live_ai_bot = ailive.live_ai_bot:main',
        ]
  ),
)

