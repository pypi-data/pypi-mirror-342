# FPowerKit 配电网运算组件
**本仓库已上线PyPI**，您可以通过`pip install fpowerkit`直接以Python包的形式安装使用本仓库的代码！

这个项目是[V2Sim](https://gitee.com/fmy_xfk/v2sim)的附属项目。V2Sim的论文请见arXiv: https://arxiv.org/abs/2412.09808

IEEE33和IEEE69节点的配网数据从公开渠道收集。除配网数据以外，本仓库代码均遵循LGPL3.0协议使用。

## 简介
- 依赖于feasytools和gurobipy: `pip install feasytools gurobipy`（请自行安装Gurobi并申请许可证）
- 包含电网的描述(含母线、发电机、线路等)和采用Gurobi的配电网DistFlow模型求解。
- 优化目标为“发电成本最小”。发电成本模型为二次函数$f(x)=ax^2+bx+c$。
- 内含IEEE 33节点配电网和IEEE 69节点配电网，可通过以下方式快速创建：
```py
from fpowerkit import PDNCases
grid_obj33 = PDNCases.IEEE33()
grid_obj69 = PDNCases.IEEE69()
```

## 使用

克隆本仓库，并输入以下命令开始求解:

```bash
python main.py -g cases/33base.xml
```

请注意上述命令不适用于pip安装的版本。

`33base`描述了IEEE 33节点配电网模型。换成`3nodes`则是一个极简版3节点辐射形配电网模型，结构如下：

```
G0  G1
|   |
B0->B1->B2
    |   |
    L1  L2
```

您也换成自己的配电网文件来求解，例如`python main.py -g path/to/your_zipfile.zip`

## 配电网文件格式
[XML格式](docs/xml_file.md)

ZIP格式已经不再支持。
