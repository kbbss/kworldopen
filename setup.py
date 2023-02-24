from setuptools import setup, find_packages

setup(
   name='kls',
   version='0.0.1',
   description='klsworld open!',
   author='kebiat',
   url="https://github.com/kbbss/kworldopen.git",
   author_email='kebiat@naver.com',
   packages=find_packages(where=''),
   license="kebiat",
   zip_safe=False,
   install_requires = ["pymongo==3.12.0"]

)