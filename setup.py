from setuptools import setup, find_packages
setup(
    name="getchan",
    version="0.1.0",
    description="Somechan thread downloader.",
    url="https://github.com/rudzha/getchan",
    author="rudzha",
    author_email="rudzha@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Topic :: Communications :: BBS"
    ],
    packages=find_packages(),
    install_requires=['requests', 'toolz'],
    entry_points={
        'console_scripts':[
            'getchan=getchan.main:main'
        ]
    }
)