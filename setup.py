import os
from setuptools import setup, find_packages

setup(
    name='django-cms-menupreview',
    version='0.1',
    description='Menu previews for django CMS administration',
    author='Keryn Knight',
    author_email='github@kerynknight.com',
    license = "BSD License",
    keywords = "django",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://github.com/kezabelle/django-cms-menupreview/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['django>=1.3', 'django-cms>=2.2'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Text Processing :: Markup :: HTML',
        'License :: OSI Approved :: BSD License',
    ],
    platforms=[
        'OS Independent'
    ],
)
