# PolyContract Engine (多语种智能合同引擎)

![LuaLaTeX](https://img.shields.io/badge/Engine-LuaLaTeX-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)
![Language](https://img.shields.io/badge/language-Multilingual-orange.svg?style=flat-square)
![Scale](https://img.shields.io/badge/Ready_For-Web_Integration-success.svg?style=flat-square)

English | [中文文档](README_zh.md)

**PolyContract Engine** 是一个完全程序化、模块化和高度可扩展的法律文件与合同生成引擎，基于 LuaLaTeX 原生构建。

本项目专门为 **Web 全栈应用提供底层文档渲染支持** 而设计，彻底将数据逻辑与物理排版分离。我们的愿景是支持海量合同种类（租房、保密协议 NDA、劳动合同等）及全球各类语言配置，并实现极具美感的双语对照排版。

<p align="center">
  <img src="docs/screenshot.jpg" alt="PolyContract Preview" width="600" style="border: 1px solid #ddd; border-radius: 8px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);"/>
</p>

## 核心特性
- **专为 Web 打造的 JSON 驱动架构:** 前后端应用只需负责推送 JSON Payload，无需再依赖笨重且容易出错的字符串模板引擎。底层通过纯正 Lua 脚本直接将 Web 数据桥接进入严苛的 LaTeX 排版系统。
- **无限模块化拓展:** 底层架构旨在支持成百上千种条款模块 (`modules/`)。编译期通过 `\directlua` 执行的 `loader.lua` 解析器，自动处理并构建 LaTeX 变量、智能循环遍历多用户数组并进行条件拼接。
- **极致国际化排版支持:** 深度集成 `polyglossia` 语言配置与 `paracol` 分栏包，能够完美且无瑕疵地渲染符合严格国际化标准的双语（例如中英、捷英）对照法律文件。
- **智能化隔离构建:** 强大的 `build.sh` 脚本可自动解析注入的 JSON，提取关键用户信息生成动态物理文件名（例：`Contract_Taylor_Swift.pdf`），并严格管控所有 LaTeX 编译副产物，将其沙盒隔离在 `dist/` 目录之中，保持源码绝对纯洁。

## 战略路线图
- [ ] **合同法务库扩充:** 加入完善的 保密协议 (NDA)、劳动雇佣合同、房屋买卖合同 等模块支持。
- [ ] **高层 REST API 封装:** 构建轻量级后端 (Node.js/Python)，实现纯净的 `POST /api/generate` 接口流式返回生成的 PDF 缓冲数据。
- [ ] **Web 客户端支持:** 开发极具现代化 UI 的前端管理面板 (React/Vue) 用以动态可视化填写/编排 `data.json` 结构。

## 目录结构
```text
latex-rental-contract/
├── data.json               # 定义所使用的语言、模块选择以及详细配置数据
├── Makefile                # 自动构建工具
├── src/                    
│   ├── main.tex            # LaTeX 核心文件 
│   ├── loader.lua          # 核心 Lua 逻辑，将 JSON 内容转化为 LaTeX 指令
│   ├── styles.sty          # 全局样式、多语言排版及页边距设定 
│   └── modules/            # 依据 ISO 语言区域划分的各类法务条款 (cz/en)
└── dist/                   # 最终生成的 PDF 合同存放目录 
```

## 快速开始

### 环境依赖
您需要安装完整且包含 LuaLaTeX 的 TeX 环境。
- **macOS:** `brew install --cask mactex` 或通过 MacPorts `sudo port install texlive-luatex`
- **Linux:** `sudo apt install texlive-full`

### 使用方法
1. 从 Web 客户端推送最新信息或手动编辑 `data.json`。
2. 在项目根目录的终端中执行以下命令:
```bash
make clean
make all
```
3. 在 `dist/` 目录中即可获取带有租客名称的优质排版最终 PDF: `Contract_<TenantName>.pdf`！

## 许可协议
本项目基于 MIT 协议开源。
