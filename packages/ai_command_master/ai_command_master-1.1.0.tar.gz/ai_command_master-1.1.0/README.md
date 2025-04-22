# AI Command Master

一个基于AI的命令行工具，帮助用户更高效地完成命令行操作。

## 功能特点

- 支持多种AI模型配置（OpenAI、Deepseek、智谱AI等）
- 智能命令解析和执行（自然语言转命令行）
- 多配置文件管理（支持环境隔离）
- 跨平台支持（Windows/macOS/Linux）

## 典型场景

- 快速查询复杂命令语法
- 自动化重复性运维操作
- 安全执行危险命令前确认
- 开发环境快速配置

## 安装

### 环境要求

- Python >= 3.8（建议3.13.0）
- pip 23.0+（Python包管理器）
- Git 2.30+（源码安装需要）

### 安装步骤

#### 方法一：通过pip安装（推荐）

使用清华PyPI镜像加速安装：
```bash
pip install ai-command-master -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 方法二：从源码安装

1. 克隆项目代码：
```bash
git clone https://gitee.com/yourusername/ai-command-master.git
cd ai-command-master
```

2. 安装依赖（使用镜像源）：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple .
```

## 快速开始

### 1. 创建配置文件

```bash
# Windows系统需要以管理员模式运行CMD/PowerShell
# myconfig为文件名，建议使用model名命名
ai config create myconfig
```

### 2. 配置文件示例
```bash
# 请以官方提供的API文档为准
model_provider = "Moonshot"
model_name = "moonshot-v1-8k"
base_url = "https://api.moonshot.cn/v1"
api_key = "your_api_key"
max_token: 8192
temperature: 0.3
```

### 3. 配置文件管理

```bash
# 列出所有配置文件
ai config list

# 显示当前配置
ai config show

# 切换配置文件
ai config switch myconfig
```

## 使用指南

### 基础使用
```bash
# 获取帮助
ai --help

# 执行命令（Windows路径示例）
ai ask 如何批量重命名当前目录下所有.txt文件为.md文件？
```

## 开发说明

### 环境配置（Windows）

1. 创建虚拟环境：
```powershell
python -m venv venv
venv\Scripts\activate
```

2. 安装包：
```bash
# 使用.virtualenv文件安装所有依赖
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple e .

```

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情