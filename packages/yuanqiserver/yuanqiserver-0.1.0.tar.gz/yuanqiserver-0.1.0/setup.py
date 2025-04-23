from setuptools import setup, find_packages

str_version = '1.0.0'

setup(name='yuanqiserver',
      version=str_version,
      description='A mcp server',
      author='yuanqi_mcp163',
      author_email='yuanqi_mcp_test@163.com',
      license_text='MIT',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=['mcp', 'httpx', 'uvicorn'],
      python_requires='>=3.12')
