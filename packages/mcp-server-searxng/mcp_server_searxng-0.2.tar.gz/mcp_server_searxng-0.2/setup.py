from setuptools import setup, find_packages

# 读取 README.md 作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mcp_server_searxng',
    version='0.2',
    license='MIT',
    description='基于MCP技术的SearXNG搜索引擎服务器',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='panxingfeng',
    author_email='1115005803@qq.com',
    url='https://github.com/panxingfeng/mcp_server_searXNG',
    download_url='https://github.com/panxingfeng/mcp_server_searXNG/archive/refs/tags/0.1.tar.gz',
    
    packages=find_packages(),
    keywords=['searXNG', 'mcp', 'search', 'automation'],
    
    install_requires=[
        'mcp>=1.6.0,<2.0.0',
        'requests>=2.28.0'
    ],
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',  # 替换无效的分类器
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.11',
        'Natural Language :: Chinese (Simplified)',
    ]
)