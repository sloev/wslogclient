from distutils.core import setup
import os

setup(
        name="wslogclient",
        version="0.0.4",
        packages=["wslogclient",],
        requires = ['websocket', 'termcolor'],
        license="MIT",
        description="websocket client for logs",
        long_description=open("README").read(),
        maintainer="sloev",
        maintainer_email="johannesgj@gmail.com",
        url="http://github.com/sloev/wslogclient"
        )
