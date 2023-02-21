## 新机安装

```
# 先创建python3.10虚拟环境
conda create --prefix ./env python=3.10

# 根据yml更新这个虚拟环境
conda env --prefix ./env --file conda.yml --prune
```

如果conda安装不成功

```
# 激活当前虚拟环境
conda activate ./env

# 根据pip包安装
pip install -r pip.txt
```