import setuptools

setuptools.setup(
    name="trdicom",  # 模块名称
    version="0.0.3",  # 当前版本
    author="thorraythorray",  # 作者
    author_email="thorraythorray@gmail.com",  # 作者邮箱
    description="",  # 模块简介
    long_description='',  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'pynetdicom',
        'pydicom',
    ],
    python_requires='>=3',
    include_package_data=True,
)
