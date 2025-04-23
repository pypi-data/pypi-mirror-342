# WebSocket 接口自动化测试工具 (WS_API_TEST)

#### 介绍

这是一个基于 WebSocket 协议的接口自动化测试工具。它可以用于自动化测试 WebSocket 接口，确保接口的稳定性和可靠性。

#### 系统要求

**Python 3.10+**：确保你的系统上已经安装了 Python 3.10（推荐使用最新稳定版）。
**项目依赖**：项目需要一些第三方库，可以通过 requirements.txt 文件安装。

#### 安装步骤

**1.安装 Python：**
确保你的系统上已经安装了 Python 3.10 或更高版本。你可以从 [Python 官方网站 ](https://www.python.org/downloads/?spm=5176.28103460.0.0.40f75d27PnqPkU)下载并安装。
**2.克隆项目：**
使用 Git 克隆项目到你的本地机器。

```
git clone https://code.iflytek.com/ZNQC_AUTO_AI/python_scripts.git
cd python_scripts
git checkout WS_API_TEST
```

**3.安装项目依赖：**
使用 pip 安装项目所需的依赖库。

```
pip install -r requirements.txt
```
**4.运行项目：**
你可以通过以下两种方式之一来运行项目：

* **使用命令行**：
  在命令行中运行以下命令：

```
python run_tests.py --env uat --app 3d7d3ea4  --service gateway_5.4 --project vwa
```

* **使用批处理脚本**：
  双击 run_tests.bat 文件来运行项目。

#### 项目结构
├─allure_report
├─allure_results
├─build
├─common
├─config
├─data
├─dist
├─logs
├─testcase

* **文件说明**:
**allure_report**：存放 Allure 生成的 HTML 报告，用于展示测试结果。
**allure_results**：存放 Allure 生成的测试结果数据文件，如 result-12345.xml。
**build**：存放构建过程中生成的临时文件
**common**：存放通用的工具类
**config**：存放环境配置文件
**data**：存放测试数据文件
**dist**：存放最终发布的测试包
**logs**：存放运行日志文件
**testcase**：存放测试用例脚本
