from setuptools import setup, find_packages, Extension

setup(  
    name = "xxx", 
    version = "1.0", 
    keywords = ("tools",), 
    description = "x tools", 
    long_description = "x tools",
    license = "MIT Licence", 
    
    url = "https://github.com/vtheno/xxx", 
    author = "vtheno", 
    author_email = "a2550591@gmail.com", 
    
    packages = find_packages(), 
    include_package_data = True, 
    platforms = "any", 
    setup_requires = ['setuptools'],
    install_requires = [], 
    scripts = [], 
    entry_points = { } ,
    ext_modules = [
    ],
) 
