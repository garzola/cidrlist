from distutils.core import setup


setup(
    name = "cidrlist",
    version = "0.1",
    author = "Gustavo Arzola",
    author_email = "gustavo@xcode.com",
    maintainer = "Gustavo Arzola",
    maintainer_email = "gustavo@xcode.com",
    url = "https://bitbucket.org/garzola/cidrlist",
    description = "Classless Internet Domain Routing list implementation",
    long_description = open('README.md', 'rt').read(),

    py_modules = ['cidrlist',],
# install_requires=[
#        "ipaddr >= 4.1.11",
#        ],
    )