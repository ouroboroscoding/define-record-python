from setuptools import setup

with open('README.md', 'r') as oF:
	long_description=oF.read()

setup(
	name='record-oc',
	version='1.0.0',
	description='Provides abstract classes meant to represent record data as Define Node types',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://ouroboroscoding.com/record',
	project_urls={
		'Documentation': 'https://ouroboroscoding.com/record',
		'Source': 'https://github.com/ouroboroscoding/record-python',
		'Tracker': 'https://github.com/ouroboroscoding/record-python/issues'
	},
	keywords=['data','define','database','db','sql','nosql'],
	author='Chris Nasr - Ouroboros Coding Inc.',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['record'],
	python_requires='>=3.10',
	install_requires=[
		"define-oc>=1.0.0,<1.1",
		"jsonb>=1.0.0,<1.1",
		"tools-oc>=1.2.2,<1.3",
		"undefined-oc>=1.0.0,<1.1"
	],
	test_suite='tests',
	zip_safe=True
)