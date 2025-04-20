from setuptools import setup, find_packages

setup(
    name='api_user',  # The final package name
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask',  # Required dependencies
    ],
    python_requires='>=3.6',
    author='Baskar',
    author_email='newtonbaskar04@gmail.com',
    description='A Flask module to interact with APIs and handle user authentication.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Baskar245/api_user',  # Update with your GitHub link
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
