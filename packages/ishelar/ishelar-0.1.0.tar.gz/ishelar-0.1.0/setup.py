from setuptools import setup

setup(
    name='ishelar',
    version='0.1.0',
    description='Like antigravity, but opens your portfolio.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Saurabh Shelar',
    author_email='mr.saurabhshelar@gmail.com',
    url='https://www.saurhub.in/',
    packages=['ishelar'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
