from setuptools import setup, find_packages

setup(
    name='cmsplugin-blocks',
    version=__import__('cmsplugin_blocks').__version__,
    description=__import__('cmsplugin_blocks').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='dthenon@emencia.com',
    url='https://github.com/emencia/cmsplugin-blocks',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django>=1.9,<1.12',
        'django-cms>=3.4',
        'djangocms-text-ckeditor',
        'sorl-thumbnail',
    ],
    include_package_data=True,
    zip_safe=False
)
