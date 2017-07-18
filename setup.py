from setuptools import setup

install_requires=[
   'pandas',
   'matplotlib',
   'seaborn',
   'biomart',
   'pymysql'
]

setup(name='cbio',
      version='0.1.1',
      description='Package with bioinformatical utilities',
      url='https://github.com/Cristian-pg/cbio',
      author='Cristian Perez',
      author_email='Vilero89@gmail.com',
      license='GNU General Public License v3.0',
      packages=['cbio'],
      zip_safe=False)
