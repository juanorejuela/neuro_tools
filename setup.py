from setuptools import setup, find_packages

setup(
	name='neuro_tools',
	version='0.1',
	packages=find_packages(),
	install_requires=[
		'numpy',
		'pandas',
		'scipy',
		'nibabel',
		'nilearn',
		'matplotlib'
	],
	entry_points={
		'console_scripts': [
			'extract_ts=bin.extract_ts:main',
		],
	},
)
