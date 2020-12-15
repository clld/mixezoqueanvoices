from setuptools import setup, find_packages


setup(
    name='mixezoqueanvoices',
    version='0.0',
    description='mixezoqueanvoices',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clld',  # >=7.0
        'clld-audio-plugin>=0.2',
        'clldmpg',
        'pyglottolog',

],
extras_require={
        'dev': ['flake8', 'waitress'],
        'test': [
            'pytest>=5.4',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="mixezoqueanvoices",
    entry_points="""\
    [paste.app_factory]
    main = mixezoqueanvoices:main
""")
