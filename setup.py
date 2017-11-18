from setuptools import setup

setup(
    name='hamming_app',
    py_modules = ['flask_app.py', 'hammingclasses.py'],
    # packages=['flask_app', 'hammingclasses'],
    include_package_data=True,
    install_requires=[
        'flask',
        'numpy'
    ],
)