import distutils.core

version = '0.1.3'

distutils.core.setup(
	name='mingdao',
	version=version,
    keywords = ('mingdao', 'oauth2'),
	packages=['mingdao'],
    package_dir={'mingdao':'mingdao'},
    package_data={'mingdao':['data/*.json']},
	author='Sin',
	author_email='sin.zou@mindao.com',
	url='http://github.com/ipy/api_python',
	description='Python SDK for mingdao.com, provides Mingdao OAuth2 authorization and API wrapper.',
    long_description = open('README.md').read(),
	install_requires=[
		'requests',
	],
	classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Bottle",
    ],
)
