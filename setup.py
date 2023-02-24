from setuptools import setup, find_packages

setup(
   name='klswordopen',
   version='0.0.1',
   description='klsworld open!',
   author='kebiat',
   url="https://github.com/kbbss/kworldopen.git",
   author_email='kebiat@naver.com',
   packages=['osul'],  # would be the same as name
   license="kebiat",
   zip_safe=False,
   install_requires = ["pymongo==3.12.0"]

)