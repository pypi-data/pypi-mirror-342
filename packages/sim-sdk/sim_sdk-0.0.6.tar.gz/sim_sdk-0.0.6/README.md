# datacenter-python

#### 介绍
数据闭环平台数据处理Python脚本


#### sim-sdk
项目根目录下
1. 配置的setup.py文件
2. 安装构建sdk工具环境：pip install --upgrade build twine  
3. 构建sdk：python -m build 
4. 上传sdk：twine upload dist/*

#### 本地build和安装sim-sdk，不上传
1. python setup.py sdist bdist_wheel
2. 卸载：pip uninstall sim-sdk
3. 本地安装：pip install .\dist\sim_sdk-0.0.2.tar.gz

#### build 开发docker 
根目录/debug
1. Dockerfile 中包含install sim-sdk：pip install --no-cache-dir --index-url https://pypi.org/simple sim-sdk==0.0.2
2. 镜像分发给算子开发人员

