from setuptools import setup, find_packages
with open('PyPI/README.md') as readme_file:
    README = readme_file.read()
with open('PyPI/HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = {'name': "onemapsg",
              'version': "1.0.1",
              'description': "Python Wrapper Client for the OneMap API with automatic token handling",
              'long_description_content_type': "text/markdown",
              'long_description': README + '\n\n' + HISTORY,
              'license': "MIT",
              'packages': find_packages(),
              'author': "methylDragon",
              'author_email': "methylDragon@gmail.com",
              'keywords': ['onemap', 'api'],
              'url': "https://github.com/methylDragon/one-map-api-client",
              'download_url': "https://pypi.org/project/onemapsg/"}

install_requires = ['requests>=2.20.0', 'requests_toolbelt']

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
