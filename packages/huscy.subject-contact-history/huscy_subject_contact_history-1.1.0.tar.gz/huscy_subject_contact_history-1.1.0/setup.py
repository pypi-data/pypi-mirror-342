from setuptools import find_namespace_packages, setup

from huscy.subject_contact_history import __version__


setup(
    name="huscy.subject_contact_history",
    version=__version__,
    license='AGPLv3+',

    author='Stefan Bunde',
    author_email='stefanbunde+git@posteo.de',

    packages=find_namespace_packages(include=['huscy.*']),

    install_requires=[
        'huscy.projects',
        'huscy.pseudonyms',
        'huscy.subjects',
    ],
    extras_require={
        'development': ['psycopg2-binary'],
        'testing': ['tox', 'watchdog'],
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
    ],
)
