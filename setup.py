from setuptools import setup, find_packages

setup(
   name='kls',
   version='0.0.1',
   description='klsworld open!',
   author='kebiat',
   url="https://github.com/kbbss/kworldopen.git",
   author_email='kebiat@naver.com',
   packages=find_packages(where='src'),
  package_dir={'': 'src'},
   license="kebiat",
   zip_safe=False,
   install_requires = ["pymongo"]

)

#,"flask","flask-ngrok","pyngrok==4.1.1"