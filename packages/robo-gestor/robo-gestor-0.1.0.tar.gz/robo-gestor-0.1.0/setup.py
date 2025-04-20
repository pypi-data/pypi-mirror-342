from setuptools import setup, find_packages

setup(
    name='robo-gestor',  # Replace with your package name
    version='0.1.0',  # Update with the current version
    packages=find_packages(),  # Automatically discovers packages in the directory
    description='A Python automation utility for interacting with Android devices via uiautomator2.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rohit Kumar',
    author_email='mailrohitkr6@gmail.com',
    url='https://github.com/RohitKumarGit/RoboGestor',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python version compatibility
    install_requires=[
        'uiautomator2',  # Your package dependencies
    ],
    include_package_data=True,  # Ensure non-Python files (like README) are included
)
