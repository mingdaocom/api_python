import distutils.core

version = '0.1'

distutils.core.setup(
	name='mingdao',
	version=version,
	packages=['mingdao'],
	author='Sin',
	author_email='sin.zou@mindao.com',
	url='http://github.com/ipy/api_python',
	description='Python SDK for mingdao.com, provides Mingdao OAuth2 authorization and API wrapper.',
	classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Bottle",
    ],
)