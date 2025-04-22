from setuptools import setup, find_packages

setup(
    name="sim-sdk",
    version="0.0.6",
    author="ZhiZi-jack",
    description="qtest环境",
    packages=find_packages(
        where="src",
        include=["evaluat*", "util*", "dags*"]  # 注意去掉src前缀
    ),
    package_dir={"": "src"},  # 只从src目录查找包
    py_modules=[           # 单独包含根目录的工具类
        "const_key",
        "data_deal_util",
        "es_util",
        "git_util",
        "git_util_dev",
        "label_util",
        "log_manager",
        "operator_framework",
        "operator_interface",
        "redis_util",
        "scene_util",
        "env_manager",
        "debug_task",
        # ...其他要包含的.py文件（不带扩展名）
    ],

    # 确保工具类能被找到（关键配置！）
    package_data={
        "": ["*.py"],  # 包含根目录的所有.py文件
    },

    install_requires=[
        "elasticsearch==7.11.0",
        "esdk-obs-python==3.23.12",
        "pymysql==1.1.1",
        "pyarrow==15.0.2",
        "pandas==2.2.1",
        "numpy==1.26.4",
        "redis==5.0.3",
        "minio==7.2.7",
        "requests==2.32.0",
        "nacos-sdk-python==1.0.0",
        "pyyaml==6.0.2",
        "protobuf==5.27.3",
        "ffmpeg-python==0.2.0"
        # 其他依赖...
    ],
    python_requires=">=3.9",
)