from setuptools import setup, find_packages

setup(
    name='yesdomaininfo',
    version='2.0.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'requests',
        'dnspython', 
        'python-whois',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'yesdomaininfo=yesdomainfinder.cli:main',
        ],
    },
    author='YesVanshz',
    description='Professional Domain Investigation Tool',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yesvanshzoffical/yesdomainfinder',
    python_requires='>=3.6',
)