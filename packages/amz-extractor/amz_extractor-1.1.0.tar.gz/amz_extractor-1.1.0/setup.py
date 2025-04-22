from distutils.core import setup

setup(name='amz_extractor',
      version='1.1.0',
      description='提取亚马逊详情页和评论信息',
      author='lonely',
      packages=['amz_extractor'],
      package_dir={'amz_extractor': 'amz_extractor'},
      install_requires=['dateparser>=1.1.4', 'pyquery>=1.4.3']
      )

"""
# 更新版本命令

python setup.py sdist bdist_wheel

twine upload dist/*


pypi-AgEIcHlwaS5vcmcCJDE5NjBlMTNhLWZhZjEtNGRkNC1iZTlhLTk1YjRiNmYxNTY5YwACFVsxLFsiYW16LWV4dHJhY3RvciJdXQACLFsyLFsiMTc1MjU0ZTEtZGUzOS00YTU1LWJlNTMtYmNkNDlhNjVjZmIzIl1dAAAGIO95E4ofjofr9XptMIzdFnZ_vm0OjgoJXXV5Xebu98w3
"""