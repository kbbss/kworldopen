from setuptools import setup, find_packages

setup(
   name='klswordopen',
   version='0,9,1',
   description='Something different',
   author='kebiat',
   url="https://github.com/kbbss/kworldopen.git",
   author_email='kebiat@naver.com',
   packages=['osul'],  # would be the same as name
   zip_safe=False,
   install_requires = ["pymongo==3.12.0"]

)