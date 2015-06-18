from setuptools import setup, find_packages


with open('README.rst') as readme:
    long_description = ''.join(readme).strip()


setup(
    name='openvpn-status',
    version='0.1.0.dev0',
    url='https://github.com/tonyseek/openvpn-status',
    author='Jiangge Zhang',
    author_email='tonyseek@gmail.com',
    description='Parse OpenVPN status logs in Python',
    long_description=long_description,
    packages=find_packages(),
    classifiers=[
    ],
    install_requires=[
        'humanize',
    ],
)
