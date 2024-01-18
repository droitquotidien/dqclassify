import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()

requires = [
    'ply',  # https://www.dabeaz.com/ply/index.html
    ]

tests_require = [
    'pytest',
    'pytest-cov',
    ]

setup(name='dqclassify',
      version='0.1.0',
      description='classify paragraphs to find modification instructions',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
      ],
      author='georges-andre.silber@minesparis.psl.eu',
      author_email='georges-andre.silber@minesparis.psl.eu',
      url='',
      keywords='paragraphs alineas',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [console_scripts]
      dqclassify_csv = dqclassify.scripts.classify_csv:main
      dqclassify_test_csv = dqclassify.scripts.test_csv:main
      """,
)
