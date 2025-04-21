# 星梦（xmpy）框架的CTP底层接口

## 说明

基于CTP期货版的6.7.7接口封装开发，接口中自带的是【穿透式实盘环境】的dll文件。

## 安装

直接使用pip命令：

```
pip install xmpy_ctp
```

或者下载源代码后，解压后在cmd中运行：

```
pip install .
```

使用源代码安装时需要进行C++编译，因此在执行上述命令之前请确保已经安装了【Visual Studio（Windows）】、【GCC（Linux）】、【XCode（Mac）】编译器。

如果需要以**开发模式**安装到当前Python环境，可以使用下述命令：

```
pip install -e . --no-build-isolation --config-settings=build-dir=.npy_ctpapi
```