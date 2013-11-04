"""
django-simple-formwizard
-----------------

Simple session based form wizard for django applications.

"""
from setuptools import setup, find_packages


setup(
    name='django-simple-formwizard',
    version='0.1',
    url='https://github.com/aisayko/django-simple-formwizard',
    license='MIT License',
    author='Alex Isayko',
    author_email='alex.isayko@gmail.com',
    description='Simple session based form wizard for django applications.',
    keywords = "django form wizard formwizard",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
