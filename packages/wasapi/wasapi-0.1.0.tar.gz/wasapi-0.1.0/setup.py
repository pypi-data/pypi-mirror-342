from setuptools import setup, find_packages

setup(
    name='wasapi',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'wasapi=wasapi:run',
        ],
    },
    author='ucea-cse-2026',
    author_email='newtonbaskar04@gmail.com',
    description='A simple REST API using Flask',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/wasapi',  # (optional)
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
