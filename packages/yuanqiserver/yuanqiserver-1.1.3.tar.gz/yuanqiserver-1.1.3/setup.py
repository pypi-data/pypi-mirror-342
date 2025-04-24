from setuptools import setup, find_packages

str_version = '1.1.3'

setup(name='yuanqiserver',
      version=str_version,
      description='A mcp server',
      author='yuanqi_mcp163',
      author_email='yuanqi_mcp_test@163.com',
      license_text='MIT',
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            # 定义命令行工具，用户运行 uvx your-mcp-server 时会执行 your_mcp_server.main:main
            'yuanqiserver=yuanqiserver.main:main',
        ],
      },
      zip_safe=False,
      include_package_data=True,
      install_requires=['mcp', 'httpx', 'uvicorn'],
      python_requires='>=3.10')
