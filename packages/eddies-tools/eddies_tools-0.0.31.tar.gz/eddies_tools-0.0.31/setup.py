from setuptools import setup, find_packages
fp='pyproject.toml'
with open(fp,'r') as fl:
    for ln in fl.readlines():
        if ln.find('version')==0:
            version=ln.split('=')[1].strip('" \n')
            break
print(version)
import os
print(os.getcwd())
dist_dir='E:/code/eddies_tools/dist'
for f in os.listdir(dist_dir):
    fp=os.path.join(dist_dir,f)
    print('rmv',fp)
    try:
        os.remove(fp)
    except PermissionError as e:
        print(e)
setup(
    name='eddies_tools',
    version=version,
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    include_package_data=True,  # This line is important
)