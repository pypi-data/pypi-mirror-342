from setuptools import setup, find_packages

setup(
    name='Django-logins-users',
    version='0.1.1',
    author='djangoUser',
    author_email='django4234@gmail.com',
    description='django-authUser',
    long_description=open('README.md').read(),
    license_file='OSI Approved :: MIT License',
    long_description_content_type='text/markdown',
    url='https://github.com/delss28/Django-auths.git',  
    packages=find_packages(),
    package_data={
        'Django_auths': ['slaveni/*'],  
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)