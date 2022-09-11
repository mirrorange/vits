# VITS

这是一个带有 WebAPI ，支持多个模型的 VITS.

## 使用方法
- 安装 Python3.6 以上版本
- 安装 CMake
- 安装依赖 `pip install -r requirements.txt`
- 安装 ESpeak `apt-get install espeak`
- 编译 monotonic_align 
```
cd monotonic_align 
mkdir monotonic_align
python setup.py build_ext --inplace
```
- 下载模型文件，命名为 model.pth 和 config.json 放入对应模型文件夹
- 运行API服务器 `python api.py`