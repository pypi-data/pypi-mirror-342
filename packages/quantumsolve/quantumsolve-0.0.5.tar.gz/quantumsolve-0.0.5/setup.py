from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]


with open('README.txt', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='quantumsolve',
    version='0.0.5',
    description='Famous math, physics, stats, and CS equations as Python functions.',
    long_description=long_description,
    long_description_content_type='text/plain', 
    url='',  
    author='Md Muzahidul Islam',
    author_email='muzahidsife@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator equations math physics statistics computer science',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
)
#Remove-Item -Recurse -Force dist, build, *.egg-info
#py setup.py sdist bdist_wheel
#twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDIyOGMyYTkxLTA1NDctNGRkNC1iMmE3LWE2MTc3NjRkZWU2MAACFFsxLFsicXVhbnR1bXNvbHZlIl1dAAIsWzIsWyI2NDY1YzAyOS1hZjlkLTRiNTktYmVmMC02ODI1NmRlNTg2NzYiXV0AAAYgBKYcm_KrPoKDCd-DTtngkO4PGc1hpuBMvxqqWdtuSv8