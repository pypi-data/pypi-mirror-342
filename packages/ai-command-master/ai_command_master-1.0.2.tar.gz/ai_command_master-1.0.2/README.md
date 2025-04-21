# AI Command Master

一个基于AI的命令行工具，帮助用户更高效地完成命令行操作。

## 功能特点

- 支持多种AI模型配置（如OpenAI、Deepseek等）
- 智能命令解析和执行
- 历史记录管理
- 跨平台支持
- 可配置的代理和超时设置

## 安装

### 环境要求

- Python >= 3.8（建议3.13.0）
- pip（Python包管理器）

### 安装步骤

1. 克隆项目代码：
```bash
git clone https://github.com/yourusername/ai-command-master.git
cd ai-command-master
```

2. 安装依赖：
```bash
pip install .
# 清华PyPI站网址：https://pypi.tuna.tsinghua.edu.cn/simple
```

## 配置

使用以下命令进行交互式配置：

```bash
ai config set
```

该命令将引导您配置以下参数：
- model_provider：AI模型提供商
- model：模型名称
- base_url：API基础URL
- api_key：API密钥
- max_token：最大token数
- temperature：温度参数

您可以直接回车跳过不需要修改的配置项。所有配置将保存在用户配置文件中。

## 使用方法

安装完成后，可以通过`ai`命令来使用：

```bash
ai <your-command-or-question>
```

### 示例

```bash
# 获取帮助信息
ai --help

# 执行命令
ai 如何查看当前目录下的所有文件？
```

## 开发说明

### 项目结构

```
ai_command_master/
├── api_clients/            # AI模型客户端
├── config/                 # 配置文件
├── __init__.py             # 包初始化
├── cli.py                  # 命令行接口
├── core.py                 # 核心功能
├── execution.py            # 命令执行
└── utils.py                # 工具函数
```

### 开发环境设置

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

2. 安装开发依赖：
```bash
pip install -e .
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情