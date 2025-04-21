from setuptools import setup, find_packages

setup(
    name='TrackingEnergy',              # ชื่อที่ใช้บน PyPI
    version='0.1.2',
    description='EnergyTracker is a library for monitoring system resource usage and energy consumption. CPU, RAM, Disk,GPU and Co2',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Khomson Kocento',
    author_email='project2you@email.com',
    url='https://github.com/project2you/TrackingEnergy',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
