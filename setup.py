from setuptools import setup, find_packages
 
setup(
    name='django-newrpx',
    version='0.1.1',
    description='A full featured django rpx authentication system',
    author='soad241',
    author_email='unknown@unknown.com',
    url='http://code.google.com/p/django-newrpx/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 0 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
