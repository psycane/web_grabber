from setuptools import setup

REQUIREMENTS = ["Click",
                "Pillow",
                "hodorlive"]

CLASSIFIERS = ['Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python']

setup(
    name="web_grabber",
    version="1.0",
    description='Python library to grab data from websites',
    long_description=open('README.md').read(),
    py_modules=['grab'],
    entry_points="""
    	[console_scripts]
    	grab=grab:cli
    """,
    url='https://github.com/psycane/web_grabber',
    author='Himanshu Malhotra',
    author_email='himanshumalhotra07@gmail.com',
    license='MIT',
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    keywords='Grab from websites'
)
