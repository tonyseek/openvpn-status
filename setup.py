from setuptools import setup, find_packages


with open('README.rst') as readme:
    next(readme)  # skip badges
    long_description = ''.join(readme).strip()


setup(
    name='openvpn-status',
    version='0.1.0',
    url='https://github.com/tonyseek/openvpn-status',
    author='Jiangge Zhang',
    author_email='tonyseek@gmail.com',
    description='Parse OpenVPN status logs in Python',
    long_description=long_description,
    packages=find_packages(),
    zip_safe=False,
    license='MIT',
    keywords=['openvpn', 'status', 'log'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: Log Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    install_requires=[
        'six',
        'humanize',
    ],
    extras_require={
        ':python_version == "2.7"': [
            'ipaddress',
        ],
    },
    platforms=['Any'],
)
