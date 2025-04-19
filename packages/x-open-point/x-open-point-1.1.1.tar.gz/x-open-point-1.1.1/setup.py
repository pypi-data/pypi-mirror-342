import setuptools
import distutils.core

setuptools.setup(
    name='x-open-point',
    version="1.1.1",
    author='@readwithai',
    long_description_content_type='text/markdown',
    author_email='talwrii@gmail.com',
    description='When using X11 launch and application at a particular location',
    license='MIT',
    url='https://github.com/talwrii/x-open-point',
    install_requires=["Xlib"],
    packages=["x_open_point"],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['x-open-point=x_open_point.main:main']
    }
)
