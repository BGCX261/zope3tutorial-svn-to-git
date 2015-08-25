from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='kg.locationfield',
      version=version,
      description="Plone FormGen Field for entering a Products.Maps Location",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Kevin Gill',
      author_email='kevin@movieextras.ie',
      url='http://code.google.com/p/zope3tutorial/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['kg'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.Maps',
          'Products.PloneFormGen',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )
