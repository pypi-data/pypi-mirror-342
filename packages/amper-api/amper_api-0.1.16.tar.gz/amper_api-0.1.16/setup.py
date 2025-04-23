from setuptools import setup, find_packages
import sys


v = sys.argv[3]
sys.argv.pop()

VERSION = '0.1.' + str(int(v)-1)
DESCRIPTION = 'Amper API package'
LONG_DESCRIPTION = 'Package for communicating with Amplifier API.'

setup(
        name="amper_api",
        version=VERSION,
        author="Amplifier",
        author_email="support@ampliapps.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["python-logstash==0.4.8"],

        keywords=['amplifier', 'b2b', 'erp'],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ]
)
