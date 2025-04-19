from setuptools import setup, find_packages

setup(
    name='django-drones',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A reusable Django app for managing drone operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tom Stout',
    author_email='tom@airborne-images.net',
    url='https://github.com/yourusername/django-drones',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
