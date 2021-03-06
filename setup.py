import os
import re
import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

def find_version(fnam,version="VERSION"):
    with open(fnam) as f:
        cont = f.read()
    regex = f"{version}\s*=\s*[\"]([^\"]+)[\"]"
    match = re.search(regex,cont)
    if match is None:
        raise Exception( f"version with spec={version} not found, use double quotes for version string")
    return match.group(1)
   
def find_projectname():
    cwd = os.getcwd()
    name = os.path.basename(cwd)
    return name  
  
def setup():
    
    version = "v0.0.4"
    projectname = find_projectname()
    
    setuptools.setup(
        name=projectname,
        py_modules=[],
        version=version,        
        author="k.r. goger",
        author_email=f"k.r.goger+{projectname}@gmail.com",
        description="File Guard and Large File Guard for preserving file content",
        long_description=long_description,
        long_description_content_type="text/markdown",        
        url=f"https://github.com/kr-g/{projectname}",        
        packages=setuptools.find_packages(),
        license = 'MIT',
        keywords = 'utility test testing file handling bim '
                    +'guard before-image copy-on-write',
        install_requires=[],    
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: POSIX :: Linux',
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],
        python_requires='>=3.6',
        scripts=[],
    )

setup()
