<div align="center">

```
    ████████╗███████╗███╗   ██╗████████╗███████╗██████╗
    ╚══██╔══╝██╔════╝████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
       ██║   █████╗  ██╔██╗ ██║   ██║   █████╗  ██████╔╝
       ██║   ██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
       ██║   ███████╗██║ ╚████║   ██║   ███████╗██║  ██║
       ╚═╝   ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```

**轻量级终端音频处理 CLI 工具箱**

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![PyPI version](https://img.shields.io/pypi/v/soundforge.svg)
![Tests](https://img.shields.io/badge/Tests-passing-brightgreen.svg)

</div>

---

<a id="简体中文"></a>

# 简体中文

## 1. 🎉 项目介绍

**SoundForge** 是一款轻量级的终端音频处理命令行工具箱，专为开发者、音频爱好者和 DevOps 工程师打造。它提供了一整套音频处理能力——从格式转换、音频剪辑到可视化分析——全部在终端中完成，无需打开任何图形界面。

### 核心价值

- **零依赖安装**：核心功能仅依赖 Python 标准库，一条命令即可完成安装
- **强大音频处理**：涵盖格式转换、剪辑拼接、音量控制、频谱分析等完整功能链
- **优雅终端体验**：彩色输出、进度条、ASCII 波形图，让命令行不再枯燥

### 解决的痛点

| 痛点 | SoundForge 的方案 |
|------|-------------------|
| ffmpeg 命令参数复杂，难以记忆 | 语义化子命令，`soundforge convert` 一行搞定 |
| 缺乏统一的音频处理工具 | 集转换、编辑、分析、录制于一体的完整工具箱 |
| 现有工具依赖沉重，安装繁琐 | 核心零依赖，`pip install` 即装即用 |
| 批量处理需要编写脚本 | 内置智能批处理引擎，支持递归目录和 glob 模式 |
| 终端工具输出简陋 | 彩色 TUI 输出，ASCII 波形与频谱可视化 |

### 差异化优势

- **零依赖核心**：格式转换、音频分析等核心功能完全基于 Python 标准库实现，不依赖 ffmpeg、sox 等外部工具
- **精美 TUI 输出**：彩色终端输出、实时进度条、ASCII 波形与频谱图，带来愉悦的命令行体验
- **智能批处理引擎**：自动识别目录中的音频文件，支持 glob 模式匹配，一键批量处理

### 灵感来源

受 GitHub Trending 上音乐与音频工具的流行趋势启发，我们希望打造一款真正属于终端用户的音频瑞士军刀——简单、强大、优雅。

---

## 2. ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔊 **格式转换** | 支持 WAV、MP3、FLAC、OGG、AAC 等主流音频格式互转 |
| ✂️ **音频编辑** | 裁剪、分割、拼接、淡入淡出，精细控制音频片段 |
| 🎚️ **音量控制** | 音量标准化、增益调节、淡入淡出效果 |
| 📊 **音频分析** | 时长、采样率、声道数、响度等全方位音频信息 |
| 🎨 **可视化** | ASCII 波形图与频谱图，终端中直观感受音频 |
| 🔄 **批量处理** | 递归目录扫描、glob 模式匹配，高效批量操作 |
| 🎤 **录音功能** | 终端内录音，实时电平表显示 |
| 💻 **零依赖** | 核心功能仅使用 Python 标准库，开箱即用 |
| 🌈 **精美输出** | 彩色终端、进度条、表格化展示，告别单调黑白 |
| 🖥️ **跨平台** | 完美支持 Windows、macOS、Linux 三大平台 |

---

## 3. 🚀 快速开始

### 环境要求

- **Python 3.8+**（推荐 3.10 及以上版本）

### 安装

```bash
# 从 PyPI 安装（推荐）
pip install soundforge

# 从源码安装
git clone https://github.com/yourusername/soundforge.git
cd soundforge
pip install -e .
```

### 快速体验

```bash
# 查看音频信息
soundforge info audio.wav

# 可视化波形
soundforge visualize audio.wav

# 格式转换
soundforge convert audio.wav -o audio.mp3

# 裁剪音频（从第 10 秒到第 30 秒）
soundforge trim audio.wav -o output.wav --start 10 --end 30

# 音量标准化
soundforge normalize audio.wav -o normalized.wav

# 批量转换目录下所有音频为 MP3
soundforge batch convert ./music/ --format mp3
```

---

## 4. 📖 详细使用指南

### 4.1 `info` — 查看音频信息

显示音频文件的详细信息，包括格式、时长、采样率、比特率、声道数等。

```bash
soundforge info <音频文件路径>
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `path` | 音频文件路径（必填） | — |
| `--json` | 以 JSON 格式输出 | `false` |
| `--verbose` | 显示额外详细信息 | `false` |

**示例：**

```bash
# 基本用法
soundforge info recording.wav

# JSON 格式输出（便于脚本解析）
soundforge info recording.wav --json

# 详细模式
soundforge info recording.wav --verbose
```

### 4.2 `visualize` — 音频可视化

在终端中渲染 ASCII 波形图或频谱图。

```bash
soundforge visualize <音频文件路径> [选项]
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `path` | 音频文件路径（必填） | — |
| `--type` | 可视化类型：`waveform` / `spectrum` | `waveform` |
| `--width` | 终端显示宽度（字符数） | `80` |
| `--height` | 终端显示高度（行数） | `20` |
| `--color` | 启用彩色输出 | `true` |

**示例：**

```bash
# 波形图（默认）
soundforge visualize song.mp3

# 频谱图
soundforge visualize song.mp3 --type spectrum

# 自定义尺寸
soundforge visualize song.mp3 --width 120 --height 30
```

### 4.3 `convert` — 格式转换

将音频文件从一种格式转换为另一种格式。

```bash
soundforge convert <输入文件> -o <输出文件> [选项]
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入文件路径（必填） | — |
| `-o, --output` | 输出文件路径（必填） | — |
| `--bitrate` | 目标比特率（如 `128k`、`320k`） | 自动选择 |
| `--sample-rate` | 目标采样率（如 `44100`、`48000`） | 保持原始 |
| `--channels` | 目标声道数：`1`（单声道）/ `2`（立体声） | 保持原始 |

**示例：**

```bash
# WAV 转 MP3
soundforge convert input.wav -o output.mp3

# 指定比特率为 320kbps
soundforge convert input.flac -o output.mp3 --bitrate 320k

# 转为单声道 44100Hz
soundforge convert input.wav -o output.ogg --channels 1 --sample-rate 44100
```

### 4.4 `trim` — 裁剪音频

从音频文件中截取指定时间段的片段。

```bash
soundforge trim <输入文件> -o <输出文件> [选项]
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入文件路径（必填） | — |
| `-o, --output` | 输出文件路径（必填） | — |
| `--start` | 起始时间（秒，支持 `mm:ss` 格式） | `0` |
| `--end` | 结束时间（秒，支持 `mm:ss` 格式） | 文件末尾 |
| `--duration` | 截取时长（秒） | — |

**示例：**

```bash
# 截取第 10 秒到第 30 秒
soundforge trim audio.wav -o clip.wav --start 10 --end 30

# 截取前 60 秒
soundforge trim audio.wav -o clip.wav --duration 60

# 使用 mm:ss 格式
soundforge trim audio.wav -o clip.wav --start 1:30 --end 2:45
```

### 4.5 `normalize` — 音量标准化

自动调整音频音量至标准水平。

```bash
soundforge normalize <输入文件> -o <输出文件> [选项]
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入文件路径（必填） | — |
| `-o, --output` | 输出文件路径（必填） | — |
| `--target` | 目标响度级别（dBFS） | `-3.0` |
| `--loudness` | 使用响度标准化（LUFS） | `false` |

**示例：**

```bash
# 标准化至 -3dBFS
soundforge normalize quiet_audio.wav -o normalized.wav

# 使用 EBU R128 响度标准化
soundforge normalize podcast.wav -o podcast_loud.wav --loudness
```

### 4.6 `split` — 分割音频

将音频文件按时间点或静音段分割为多个片段。

```bash
soundforge split <输入文件> [选项]
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入文件路径（必填） | — |
| `-o, --output-dir` | 输出目录 | 当前目录 |
| `--segments` | 分割时间点（逗号分隔，如 `30,60,90`） | — |
| `--silence` | 按静音段自动分割 | `false` |
| `--min-silence` | 静音段最短时长（秒） | `0.5` |
| `--silence-threshold` | 静音检测阈值（dB） | `-40` |

**示例：**

```bash
# 按时间点分割
soundforge split album.wav --segments 180,360,540 -o ./tracks/

# 按静音段自动分割
soundforge split recording.wav --silence -o ./segments/
```

### 4.7 `concat` — 拼接音频

将多个音频文件按顺序拼接为一个文件。

```bash
soundforge concat <文件1> <文件2> ... -o <输出文件>
```

**示例：**

```bash
# 拼接多个文件
soundforge concat intro.wav main.wav outro.wav -o full.wav

# 使用通配符
soundforge concat ./parts/*.wav -o merged.wav
```

### 4.8 `fade` — 淡入淡出

为音频添加淡入或淡出效果。

```bash
soundforge fade <输入文件> -o <输出文件> [选项]
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入文件路径（必填） | — |
| `-o, --output` | 输出文件路径（必填） | — |
| `--fade-in` | 淡入时长（秒） | `0` |
| `--fade-out` | 淡出时长（秒） | `0` |
| `--shape` | 淡化曲线：`linear` / `logarithmic` / `s-curve` | `linear` |

**示例：**

```bash
# 2 秒淡入 + 3 秒淡出
soundforge fade audio.wav -o faded.wav --fade-in 2 --fade-out 3

# 使用 S 型曲线
soundforge fade audio.wav -o faded.wav --fade-in 1.5 --shape s-curve
```

### 4.9 `record` — 终端录音

直接在终端中录制音频，并显示实时电平表。

```bash
soundforge record -o <输出文件> [选项]
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-o, --output` | 输出文件路径（必填） | — |
| `-d, --duration` | 录制时长（秒） | 按 Ctrl+C 停止 |
| `--sample-rate` | 采样率 | `44100` |
| `--channels` | 声道数 | `1` |
| `--format` | 输出格式 | `wav` |

**示例：**

```bash
# 录制 30 秒音频
soundforge record -o voice.wav -d 30

# 立体声录制
soundforge record -o stereo.wav -d 60 --channels 2
```

### 4.10 `batch` — 批量处理

对目录中的音频文件执行批量操作。

```bash
soundforge batch <子命令> <目录路径> [选项]
```

**支持的子命令：** `convert`、`normalize`、`info`、`trim`

**示例：**

```bash
# 批量转换为 MP3
soundforge batch convert ./music/ --format mp3

# 批量标准化音量
soundforge batch normalize ./podcasts/ -o ./normalized/

# 递归处理子目录
soundforge batch convert ./audio_library/ --format flac --recursive

# 使用 glob 模式筛选
soundforge batch convert ./audio/ --pattern "*.wav" --format mp3
```

### 4.11 配置选项

SoundForge 支持通过配置文件自定义默认行为。配置文件位于 `~/.soundforge/config.yaml`。

```yaml
# ~/.soundforge/config.yaml
default:
  output_format: mp3
  bitrate: 320k
  sample_rate: 44100
  channels: 2

visualize:
  width: 100
  height: 25
  color: true

batch:
  recursive: false
  overwrite: false
  parallel_jobs: 4
```

### 4.12 典型使用场景

**场景一：播客后期处理**

```bash
# 1. 查看录制信息
soundforge info podcast_raw.wav

# 2. 标准化音量
soundforge normalize podcast_raw.wav -o podcast_normalized.wav

# 3. 添加淡入淡出
soundforge fade podcast_normalized.wav -o podcast_final.wav --fade-in 1 --fade-out 2

# 4. 转换为 MP3 发布
soundforge convert podcast_final.wav -o podcast.mp3 --bitrate 128k
```

**场景二：音乐库整理**

```bash
# 批量将 FLAC 转为 MP3（节省空间）
soundforge batch convert ./flac_library/ --format mp3 --bitrate 320k

# 批量标准化音量
soundforge batch normalize ./mp3_library/ -o ./normalized/
```

**场景三：音频采样与分析**

```bash
# 可视化波形
soundforge visualize sample.wav --width 120

# 查看频谱
soundforge visualize sample.wav --type spectrum

# 导出详细信息为 JSON
soundforge info sample.wav --json > metadata.json
```

---

## 5. 💡 设计思路与迭代规划

### 设计哲学

SoundForge 遵循三大设计原则：

1. **简洁至上**：每个子命令只做一件事，参数命名直觉化，降低学习成本
2. **零依赖优先**：核心功能基于 Python 标准库实现，确保在任意环境下都能运行
3. **终端美学**：彩色输出、进度条、ASCII 可视化，让命令行工具也能赏心悦目

### 为什么优先使用 Python 标准库？

- **安装便捷**：无需安装 ffmpeg、sox 等系统级依赖，降低用户门槛
- **可移植性**：纯 Python 实现确保在所有平台上行为一致
- **可靠性**：不依赖外部工具版本，避免兼容性问题
- **可选扩展**：对于需要高级编解码的场景，支持可选安装 ffmpeg 后端

### 迭代规划

| 阶段 | 内容 | 状态 |
|------|------|------|
| v1.0 | 核心功能：格式转换、音频编辑、可视化 | ✅ 已完成 |
| v1.5 | 批量处理引擎、配置系统 | ✅ 已完成 |
| v2.0 | 插件系统、录音功能增强 | 🔨 进行中 |
| v2.5 | 更多格式支持（Opus、WMA）、AI 降噪 | 📋 规划中 |
| v3.0 | WebUI 界面、远程处理模式 | 📋 规划中 |

---

## 6. 📦 打包与部署指南

### 从 PyPI 安装

```bash
pip install soundforge
```

### 从源码安装

```bash
git clone https://github.com/yourusername/soundforge.git
cd soundforge
python -m pip install -e .
```

### 使用 Docker

```bash
# 拉取镜像
docker pull soundforge/cli:latest

# 运行容器
docker run --rm -v $(pwd):/data soundforge/cli info /data/audio.wav

# 批量处理
docker run --rm -v $(pwd):/data soundforge/cli batch convert /data/music/ --format mp3
```

### CI/CD 集成

**GitHub Actions 示例：**

```yaml
name: Audio Processing
on: [push, pull_request]

jobs:
  process-audio:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install SoundForge
        run: pip install soundforge

      - name: Process audio files
        run: |
          soundforge batch convert ./audio/ --format mp3
          soundforge batch normalize ./audio/ -o ./output/
```

---

## 7. 🤝 贡献指南

我们欢迎并感谢所有形式的贡献！无论是提交 Bug 报告、改进文档，还是贡献代码。

### 提交 Pull Request

1. **Fork** 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -m "feat: 添加某功能"`
4. 推送分支：`git push origin feature/your-feature-name`
5. 提交 **Pull Request**

**Commit 消息规范：** 遵循 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具链变更

### 提交 Issue

- 使用清晰的标题描述问题
- 附上完整的复现步骤
- 提供运行环境信息（操作系统、Python 版本、SoundForge 版本）
- 如有可能，附上相关的音频文件样本

### 开发环境搭建

```bash
git clone https://github.com/yourusername/soundforge.git
cd soundforge
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src/ tests/
ruff check src/ tests/
```

---

## 8. 📄 开源协议

本项目基于 [MIT License](https://opensource.org/licenses/MIT) 开源。

```
MIT License

Copyright (c) 2024 SoundForge Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<a id="繁體中文"></a>

# 繁體中文

## 1. 🎉 專案介紹

**SoundForge** 是一款輕量級的終端音訊處理命令列工具箱，專為開發者、音訊愛好者與 DevOps 工程師量身打造。它提供了一整套音訊處理能力——從格式轉換、音訊剪輯到視覺化分析——全部在終端中完成，無需開啟任何圖形介面。

### 核心價值

- **零依賴安裝**：核心功能僅依賴 Python 標準函式庫，一條指令即可完成安裝
- **強大音訊處理**：涵蓋格式轉換、剪輯拼接、音量控制、頻譜分析等完整功能鏈
- **優雅終端體驗**：彩色輸出、進度條、ASCII 波形圖，讓命令列不再枯燥

### 解決的痛點

| 痛點 | SoundForge 的方案 |
|------|-------------------|
| ffmpeg 指令參數複雜，難以記憶 | 語義化子命令，`soundforge convert` 一行搞定 |
| 缺乏統一的音訊處理工具 | 集轉換、編輯、分析、錄製於一體的完整工具箱 |
| 現有工具依賴沉重，安裝繁瑣 | 核心零依賴，`pip install` 即裝即用 |
| 批次處理需要撰寫腳本 | 內建智慧批次處理引擎，支援遞迴目錄與 glob 模式 |
| 終端工具輸出簡陋 | 彩色 TUI 輸出，ASCII 波形與頻譜視覺化 |

### 差異化優勢

- **零依賴核心**：格式轉換、音訊分析等核心功能完全基於 Python 標準函式庫實作，不依賴 ffmpeg、sox 等外部工具
- **精美 TUI 輸出**：彩色終端輸出、即時進度條、ASCII 波形與頻譜圖，帶來愉悅的命令列體驗
- **智慧批次處理引擎**：自動辨識目錄中的音訊檔案，支援 glob 模式比對，一鍵批次處理

### 靈感來源

受 GitHub Trending 上音樂與音訊工具的流行趨勢啟發，我們希望打造一款真正屬於終端使用者的音訊瑞士軍刀——簡單、強大、優雅。

---

## 2. ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔊 **格式轉換** | 支援 WAV、MP3、FLAC、OGG、AAC 等主流音訊格式互轉 |
| ✂️ **音訊編輯** | 裁剪、分割、拼接、淡入淡出，精細控制音訊片段 |
| 🎚️ **音量控制** | 音量標準化、增益調節、淡入淡出效果 |
| 📊 **音訊分析** | 時長、取樣率、聲道數、響度等全方位音訊資訊 |
| 🎨 **視覺化** | ASCII 波形圖與頻譜圖，終端中直觀感受音訊 |
| 🔄 **批次處理** | 遞迴目錄掃描、glob 模式比對，高效批次操作 |
| 🎤 **錄音功能** | 終端內錄音，即時電平表顯示 |
| 💻 **零依賴** | 核心功能僅使用 Python 標準函式庫，開箱即用 |
| 🌈 **精美輸出** | 彩色終端、進度條、表格化展示，告別單調黑白 |
| 🖥️ **跨平台** | 完美支援 Windows、macOS、Linux 三大平台 |

---

## 3. 🚀 快速開始

### 環境需求

- **Python 3.8+**（建議 3.10 及以上版本）

### 安裝

```bash
# 從 PyPI 安裝（推薦）
pip install soundforge

# 從原始碼安裝
git clone https://github.com/yourusername/soundforge.git
cd soundforge
pip install -e .
```

### 快速體驗

```bash
# 查看音訊資訊
soundforge info audio.wav

# 視覺化波形
soundforge visualize audio.wav

# 格式轉換
soundforge convert audio.wav -o audio.mp3

# 裁剪音訊（從第 10 秒到第 30 秒）
soundforge trim audio.wav -o output.wav --start 10 --end 30

# 音量標準化
soundforge normalize audio.wav -o normalized.wav

# 批次轉換目錄下所有音訊為 MP3
soundforge batch convert ./music/ --format mp3
```

---

## 4. 📖 詳細使用指南

### 4.1 `info` — 查看音訊資訊

顯示音訊檔案的詳細資訊，包括格式、時長、取樣率、位元率、聲道數等。

```bash
soundforge info <音訊檔案路徑>
```

**參數說明：**

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `path` | 音訊檔案路徑（必填） | — |
| `--json` | 以 JSON 格式輸出 | `false` |
| `--verbose` | 顯示額外詳細資訊 | `false` |

**範例：**

```bash
# 基本用法
soundforge info recording.wav

# JSON 格式輸出（便於腳本解析）
soundforge info recording.wav --json

# 詳細模式
soundforge info recording.wav --verbose
```

### 4.2 `visualize` — 音訊視覺化

在終端中渲染 ASCII 波形圖或頻譜圖。

```bash
soundforge visualize <音訊檔案路徑> [選項]
```

**參數說明：**

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `path` | 音訊檔案路徑（必填） | — |
| `--type` | 視覺化類型：`waveform` / `spectrum` | `waveform` |
| `--width` | 終端顯示寬度（字元數） | `80` |
| `--height` | 終端顯示高度（行數） | `20` |
| `--color` | 啟用彩色輸出 | `true` |

**範例：**

```bash
# 波形圖（預設）
soundforge visualize song.mp3

# 頻譜圖
soundforge visualize song.mp3 --type spectrum

# 自訂尺寸
soundforge visualize song.mp3 --width 120 --height 30
```

### 4.3 `convert` — 格式轉換

將音訊檔案從一種格式轉換為另一種格式。

```bash
soundforge convert <輸入檔案> -o <輸出檔案> [選項]
```

**參數說明：**

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `input` | 輸入檔案路徑（必填） | — |
| `-o, --output` | 輸出檔案路徑（必填） | — |
| `--bitrate` | 目標位元率（如 `128k`、`320k`） | 自動選擇 |
| `--sample-rate` | 目標取樣率（如 `44100`、`48000`） | 保持原始 |
| `--channels` | 目標聲道數：`1`（單聲道）/ `2`（立體聲） | 保持原始 |

**範例：**

```bash
# WAV 轉 MP3
soundforge convert input.wav -o output.mp3

# 指定位元率為 320kbps
soundforge convert input.flac -o output.mp3 --bitrate 320k

# 轉為單聲道 44100Hz
soundforge convert input.wav -o output.ogg --channels 1 --sample-rate 44100
```

### 4.4 `trim` — 裁剪音訊

從音訊檔案中截取指定時間段的片段。

```bash
soundforge trim <輸入檔案> -o <輸出檔案> [選項]
```

**參數說明：**

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `input` | 輸入檔案路徑（必填） | — |
| `-o, --output` | 輸出檔案路徑（必填） | — |
| `--start` | 起始時間（秒，支援 `mm:ss` 格式） | `0` |
| `--end` | 結束時間（秒，支援 `mm:ss` 格式） | 檔案末尾 |
| `--duration` | 截取時長（秒） | — |

**範例：**

```bash
# 截取第 10 秒到第 30 秒
soundforge trim audio.wav -o clip.wav --start 10 --end 30

# 截取前 60 秒
soundforge trim audio.wav -o clip.wav --duration 60

# 使用 mm:ss 格式
soundforge trim audio.wav -o clip.wav --start 1:30 --end 2:45
```

### 4.5 `normalize` — 音量標準化

自動調整音訊音量至標準水準。

```bash
soundforge normalize <輸入檔案> -o <輸出檔案> [選項]
```

**參數說明：**

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `input` | 輸入檔案路徑（必填） | — |
| `-o, --output` | 輸出檔案路徑（必填） | — |
| `--target` | 目標響度級別（dBFS） | `-3.0` |
| `--loudness` | 使用響度標準化（LUFS） | `false` |

**範例：**

```bash
# 標準化至 -3dBFS
soundforge normalize quiet_audio.wav -o normalized.wav

# 使用 EBU R128 響度標準化
soundforge normalize podcast.wav -o podcast_loud.wav --loudness
```

### 4.6 `split` — 分割音訊

將音訊檔案按時間點或靜音段分割為多個片段。

```bash
soundforge split <輸入檔案> [選項]
```

**參數說明：**

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `input` | 輸入檔案路徑（必填） | — |
| `-o, --output-dir` | 輸出目錄 | 當前目錄 |
| `--segments` | 分割時間點（逗號分隔，如 `30,60,90`） | — |
| `--silence` | 按靜音段自動分割 | `false` |
| `--min-silence` | 靜音段最短時長（秒） | `0.5` |
| `--silence-threshold` | 靜音檢測閾值（dB） | `-40` |

**範例：**

```bash
# 按時間點分割
soundforge split album.wav --segments 180,360,540 -o ./tracks/

# 按靜音段自動分割
soundforge split recording.wav --silence -o ./segments/
```

### 4.7 `concat` — 拼接音訊

將多個音訊檔案按順序拼接為一個檔案。

```bash
soundforge concat <檔案1> <檔案2> ... -o <輸出檔案>
```

**範例：**

```bash
# 拼接多個檔案
soundforge concat intro.wav main.wav outro.wav -o full.wav

# 使用萬用字元
soundforge concat ./parts/*.wav -o merged.wav
```

### 4.8 `fade` — 淡入淡出

為音訊添加淡入或淡出效果。

```bash
soundforge fade <輸入檔案> -o <輸出檔案> [選項]
```

**參數說明：**

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `input` | 輸入檔案路徑（必填） | — |
| `-o, --output` | 輸出檔案路徑（必填） | — |
| `--fade-in` | 淡入時長（秒） | `0` |
| `--fade-out` | 淡出時長（秒） | `0` |
| `--shape` | 淡化曲線：`linear` / `logarithmic` / `s-curve` | `linear` |

**範例：**

```bash
# 2 秒淡入 + 3 秒淡出
soundforge fade audio.wav -o faded.wav --fade-in 2 --fade-out 3

# 使用 S 型曲線
soundforge fade audio.wav -o faded.wav --fade-in 1.5 --shape s-curve
```

### 4.9 `record` — 終端錄音

直接在終端中錄製音訊，並顯示即時電平表。

```bash
soundforge record -o <輸出檔案> [選項]
```

**參數說明：**

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `-o, --output` | 輸出檔案路徑（必填） | — |
| `-d, --duration` | 錄製時長（秒） | 按 Ctrl+C 停止 |
| `--sample-rate` | 取樣率 | `44100` |
| `--channels` | 聲道數 | `1` |
| `--format` | 輸出格式 | `wav` |

**範例：**

```bash
# 錄製 30 秒音訊
soundforge record -o voice.wav -d 30

# 立體聲錄製
soundforge record -o stereo.wav -d 60 --channels 2
```

### 4.10 `batch` — 批次處理

對目錄中的音訊檔案執行批次操作。

```bash
soundforge batch <子命令> <目錄路徑> [選項]
```

**支援的子命令：** `convert`、`normalize`、`info`、`trim`

**範例：**

```bash
# 批次轉換為 MP3
soundforge batch convert ./music/ --format mp3

# 批次標準化音量
soundforge batch normalize ./podcasts/ -o ./normalized/

# 遞迴處理子目錄
soundforge batch convert ./audio_library/ --format flac --recursive

# 使用 glob 模式篩選
soundforge batch convert ./audio/ --pattern "*.wav" --format mp3
```

### 4.11 設定選項

SoundForge 支援透過設定檔自訂預設行為。設定檔位於 `~/.soundforge/config.yaml`。

```yaml
# ~/.soundforge/config.yaml
default:
  output_format: mp3
  bitrate: 320k
  sample_rate: 44100
  channels: 2

visualize:
  width: 100
  height: 25
  color: true

batch:
  recursive: false
  overwrite: false
  parallel_jobs: 4
```

### 4.12 典型使用情境

**情境一：Podcast 後期處理**

```bash
# 1. 查看錄製資訊
soundforge info podcast_raw.wav

# 2. 標準化音量
soundforge normalize podcast_raw.wav -o podcast_normalized.wav

# 3. 添加淡入淡出
soundforge fade podcast_normalized.wav -o podcast_final.wav --fade-in 1 --fade-out 2

# 4. 轉換為 MP3 發布
soundforge convert podcast_final.wav -o podcast.mp3 --bitrate 128k
```

**情境二：音樂庫整理**

```bash
# 批次將 FLAC 轉為 MP3（節省空間）
soundforge batch convert ./flac_library/ --format mp3 --bitrate 320k

# 批次標準化音量
soundforge batch normalize ./mp3_library/ -o ./normalized/
```

**情境三：音訊取樣與分析**

```bash
# 視覺化波形
soundforge visualize sample.wav --width 120

# 查看頻譜
soundforge visualize sample.wav --type spectrum

# 匯出詳細資訊為 JSON
soundforge info sample.wav --json > metadata.json
```

---

## 5. 💡 設計思路與迭代規劃

### 設計哲學

SoundForge 遵循三大設計原則：

1. **簡潔至上**：每個子命令只做一件事，參數命名直覺化，降低學習成本
2. **零依賴優先**：核心功能基於 Python 標準函式庫實作，確保在任意環境下都能運行
3. **終端美學**：彩色輸出、進度條、ASCII 視覺化，讓命令列工具也能賞心悅目

### 為什麼優先使用 Python 標準函式庫？

- **安裝便捷**：無需安裝 ffmpeg、sox 等系統級依賴，降低使用者門檻
- **可攜性**：純 Python 實作確保在所有平台上行為一致
- **可靠性**：不依賴外部工具版本，避免相容性問題
- **可選擴展**：對於需要進階編解碼的場景，支援可選安裝 ffmpeg 後端

### 迭代規劃

| 階段 | 內容 | 狀態 |
|------|------|------|
| v1.0 | 核心功能：格式轉換、音訊編輯、視覺化 | ✅ 已完成 |
| v1.5 | 批次處理引擎、設定系統 | ✅ 已完成 |
| v2.0 | 外掛系統、錄音功能增強 | 🔨 進行中 |
| v2.5 | 更多格式支援（Opus、WMA）、AI 降噪 | 📋 規劃中 |
| v3.0 | WebUI 介面、遠端處理模式 | 📋 規劃中 |

---

## 6. 📦 打包與部署指南

### 從 PyPI 安裝

```bash
pip install soundforge
```

### 從原始碼安裝

```bash
git clone https://github.com/yourusername/soundforge.git
cd soundforge
python -m pip install -e .
```

### 使用 Docker

```bash
# 拉取映像檔
docker pull soundforge/cli:latest

# 執行容器
docker run --rm -v $(pwd):/data soundforge/cli info /data/audio.wav

# 批次處理
docker run --rm -v $(pwd):/data soundforge/cli batch convert /data/music/ --format mp3
```

### CI/CD 整合

**GitHub Actions 範例：**

```yaml
name: Audio Processing
on: [push, pull_request]

jobs:
  process-audio:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install SoundForge
        run: pip install soundforge

      - name: Process audio files
        run: |
          soundforge batch convert ./audio/ --format mp3
          soundforge batch normalize ./audio/ -o ./output/
```

---

## 7. 🤝 貢獻指南

我們歡迎並感謝所有形式的貢獻！無論是提交 Bug 回報、改進文件，還是貢獻程式碼。

### 提交 Pull Request

1. **Fork** 本儲存庫
2. 建立功能分支：`git checkout -b feature/your-feature-name`
3. 提交變更：`git commit -m "feat: 新增某功能"`
4. 推送分支：`git push origin feature/your-feature-name`
5. 提交 **Pull Request**

**Commit 訊息規範：** 遵循 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

- `feat:` 新功能
- `fix:` Bug 修復
- `docs:` 文件更新
- `refactor:` 程式碼重構
- `test:` 測試相關
- `chore:` 建構/工具鏈變更

### 提交 Issue

- 使用清晰的標題描述問題
- 附上完整的重現步驟
- 提供執行環境資訊（作業系統、Python 版本、SoundForge 版本）
- 如有可能，附上相關的音訊檔案樣本

### 開發環境建置

```bash
git clone https://github.com/yourusername/soundforge.git
cd soundforge
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# 執行測試
pytest

# 程式碼格式化
black src/ tests/
ruff check src/ tests/
```

---

## 8. 📄 開源協議

本專案基於 [MIT License](https://opensource.org/licenses/MIT) 開源。

```
MIT License

Copyright (c) 2024 SoundForge Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<a id="english"></a>

# English

## 1. 🎉 Project Introduction

**SoundForge** is a lightweight terminal audio processing CLI toolbox designed for developers, audio enthusiasts, and DevOps engineers. It provides a complete suite of audio processing capabilities — from format conversion and audio editing to visualization and analysis — all within the terminal, without requiring any graphical interface.

### Core Value

- **Zero-dependency installation**: Core features rely solely on the Python standard library; install with a single command
- **Powerful audio processing**: A full pipeline covering format conversion, editing, volume control, and spectral analysis
- **Elegant terminal experience**: Colored output, progress bars, and ASCII waveform visualization that make the CLI delightful

### Pain Points Solved

| Pain Point | SoundForge's Solution |
|------------|----------------------|
| ffmpeg commands are complex and hard to remember | Semantic subcommands — `soundforge convert` gets it done in one line |
| No unified audio processing tool | An all-in-one toolbox for conversion, editing, analysis, and recording |
| Existing tools have heavy dependencies | Zero-dependency core — `pip install` and you're ready to go |
| Batch processing requires writing scripts | Built-in smart batch engine with recursive directory scanning and glob patterns |
| Terminal tool output is bare-bones | Colored TUI output with ASCII waveform and spectrum visualization |

### Differentiation

- **Zero-dependency core**: Format conversion, audio analysis, and other core features are implemented entirely with the Python standard library — no ffmpeg, sox, or other external tools required
- **Beautiful TUI output**: Colored terminal output, real-time progress bars, and ASCII waveform/spectrum charts for a pleasant CLI experience
- **Smart batch processing engine**: Automatically detects audio files in directories, supports glob pattern matching, and handles batch operations with a single command

### Inspiration

Inspired by the trending music and audio tools on GitHub, we set out to build a true Swiss Army knife for terminal users — simple, powerful, and elegant.

---

## 2. ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔊 **Format Conversion** | Convert between WAV, MP3, FLAC, OGG, AAC, and other popular audio formats |
| ✂️ **Audio Editing** | Trim, split, concatenate, and apply fade effects with precision |
| 🎚️ **Volume Control** | Normalize volume, adjust gain, and apply fade in/out effects |
| 📊 **Audio Analysis** | Comprehensive audio metadata: duration, sample rate, channels, loudness, and more |
| 🎨 **Visualization** | ASCII waveform and spectrum charts for intuitive audio inspection in the terminal |
| 🔄 **Batch Processing** | Recursive directory scanning with glob pattern matching for efficient bulk operations |
| 🎤 **Recording** | Record audio directly in the terminal with a real-time level meter |
| 💻 **Zero Dependencies** | Core features use only the Python standard library — works out of the box |
| 🌈 **Beautiful Output** | Colored terminal output, progress bars, and tabular displays — no more plain black and white |
| 🖥️ **Cross-Platform** | Full support for Windows, macOS, and Linux |

---

## 3. 🚀 Quick Start

### Requirements

- **Python 3.8+** (3.10 or later recommended)

### Installation

```bash
# Install from PyPI (recommended)
pip install soundforge

# Install from source
git clone https://github.com/yourusername/soundforge.git
cd soundforge
pip install -e .
```

### Quick Examples

```bash
# View audio info
soundforge info audio.wav

# Visualize waveform
soundforge visualize audio.wav

# Convert format
soundforge convert audio.wav -o audio.mp3

# Trim audio (from 10s to 30s)
soundforge trim audio.wav -o output.wav --start 10 --end 30

# Normalize volume
soundforge normalize audio.wav -o normalized.wav

# Batch convert all audio files to MP3
soundforge batch convert ./music/ --format mp3
```

---

## 4. 📖 Detailed Usage Guide

### 4.1 `info` — View Audio Information

Display detailed metadata for an audio file, including format, duration, sample rate, bitrate, channel count, and more.

```bash
soundforge info <audio-file-path>
```

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `path` | Path to the audio file (required) | — |
| `--json` | Output in JSON format | `false` |
| `--verbose` | Show additional detailed information | `false` |

**Examples:**

```bash
# Basic usage
soundforge info recording.wav

# JSON output (for script parsing)
soundforge info recording.wav --json

# Verbose mode
soundforge info recording.wav --verbose
```

### 4.2 `visualize` — Audio Visualization

Render ASCII waveform or spectrum charts directly in the terminal.

```bash
soundforge visualize <audio-file-path> [options]
```

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `path` | Path to the audio file (required) | — |
| `--type` | Visualization type: `waveform` / `spectrum` | `waveform` |
| `--width` | Display width in characters | `80` |
| `--height` | Display height in lines | `20` |
| `--color` | Enable colored output | `true` |

**Examples:**

```bash
# Waveform (default)
soundforge visualize song.mp3

# Spectrum
soundforge visualize song.mp3 --type spectrum

# Custom dimensions
soundforge visualize song.mp3 --width 120 --height 30
```

### 4.3 `convert` — Format Conversion

Convert an audio file from one format to another.

```bash
soundforge convert <input-file> -o <output-file> [options]
```

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `input` | Path to the input file (required) | — |
| `-o, --output` | Path to the output file (required) | — |
| `--bitrate` | Target bitrate (e.g., `128k`, `320k`) | Auto |
| `--sample-rate` | Target sample rate (e.g., `44100`, `48000`) | Preserve original |
| `--channels` | Target channel count: `1` (mono) / `2` (stereo) | Preserve original |

**Examples:**

```bash
# WAV to MP3
soundforge convert input.wav -o output.mp3

# Specify 320kbps bitrate
soundforge convert input.flac -o output.mp3 --bitrate 320k

# Convert to mono 44100Hz
soundforge convert input.wav -o output.ogg --channels 1 --sample-rate 44100
```

### 4.4 `trim` — Trim Audio

Extract a specific segment from an audio file.

```bash
soundforge trim <input-file> -o <output-file> [options]
```

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `input` | Path to the input file (required) | — |
| `-o, --output` | Path to the output file (required) | — |
| `--start` | Start time in seconds (supports `mm:ss` format) | `0` |
| `--end` | End time in seconds (supports `mm:ss` format) | End of file |
| `--duration` | Duration to extract in seconds | — |

**Examples:**

```bash
# Extract from 10s to 30s
soundforge trim audio.wav -o clip.wav --start 10 --end 30

# Extract the first 60 seconds
soundforge trim audio.wav -o clip.wav --duration 60

# Using mm:ss format
soundforge trim audio.wav -o clip.wav --start 1:30 --end 2:45
```

### 4.5 `normalize` — Volume Normalization

Automatically adjust audio volume to a standard level.

```bash
soundforge normalize <input-file> -o <output-file> [options]
```

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `input` | Path to the input file (required) | — |
| `-o, --output` | Path to the output file (required) | — |
| `--target` | Target loudness level (dBFS) | `-3.0` |
| `--loudness` | Use loudness-based normalization (LUFS) | `false` |

**Examples:**

```bash
# Normalize to -3dBFS
soundforge normalize quiet_audio.wav -o normalized.wav

# Use EBU R128 loudness normalization
soundforge normalize podcast.wav -o podcast_loud.wav --loudness
```

### 4.6 `split` — Split Audio

Split an audio file into multiple segments by time points or silence detection.

```bash
soundforge split <input-file> [options]
```

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `input` | Path to the input file (required) | — |
| `-o, --output-dir` | Output directory | Current directory |
| `--segments` | Split points (comma-separated, e.g., `30,60,90`) | — |
| `--silence` | Auto-split on silence detection | `false` |
| `--min-silence` | Minimum silence duration (seconds) | `0.5` |
| `--silence-threshold` | Silence detection threshold (dB) | `-40` |

**Examples:**

```bash
# Split at specific time points
soundforge split album.wav --segments 180,360,540 -o ./tracks/

# Auto-split on silence
soundforge split recording.wav --silence -o ./segments/
```

### 4.7 `concat` — Concatenate Audio

Merge multiple audio files into a single file in sequence.

```bash
soundforge concat <file1> <file2> ... -o <output-file>
```

**Examples:**

```bash
# Concatenate multiple files
soundforge concat intro.wav main.wav outro.wav -o full.wav

# Using wildcards
soundforge concat ./parts/*.wav -o merged.wav
```

### 4.8 `fade` — Fade In/Out

Apply fade in or fade out effects to audio.

```bash
soundforge fade <input-file> -o <output-file> [options]
```

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `input` | Path to the input file (required) | — |
| `-o, --output` | Path to the output file (required) | — |
| `--fade-in` | Fade-in duration (seconds) | `0` |
| `--fade-out` | Fade-out duration (seconds) | `0` |
| `--shape` | Fade curve: `linear` / `logarithmic` / `s-curve` | `linear` |

**Examples:**

```bash
# 2s fade in + 3s fade out
soundforge fade audio.wav -o faded.wav --fade-in 2 --fade-out 3

# Using S-curve
soundforge fade audio.wav -o faded.wav --fade-in 1.5 --shape s-curve
```

### 4.9 `record` — Terminal Recording

Record audio directly in the terminal with a real-time level meter.

```bash
soundforge record -o <output-file> [options]
```

**Parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-o, --output` | Path to the output file (required) | — |
| `-d, --duration` | Recording duration (seconds) | Stop with Ctrl+C |
| `--sample-rate` | Sample rate | `44100` |
| `--channels` | Channel count | `1` |
| `--format` | Output format | `wav` |

**Examples:**

```bash
# Record 30 seconds of audio
soundforge record -o voice.wav -d 30

# Stereo recording
soundforge record -o stereo.wav -d 60 --channels 2
```

### 4.10 `batch` — Batch Processing

Execute batch operations on audio files within a directory.

```bash
soundforge batch <subcommand> <directory-path> [options]
```

**Available subcommands:** `convert`, `normalize`, `info`, `trim`

**Examples:**

```bash
# Batch convert to MP3
soundforge batch convert ./music/ --format mp3

# Batch normalize volume
soundforge batch normalize ./podcasts/ -o ./normalized/

# Process subdirectories recursively
soundforge batch convert ./audio_library/ --format flac --recursive

# Filter with glob patterns
soundforge batch convert ./audio/ --pattern "*.wav" --format mp3
```

### 4.11 Configuration Options

SoundForge supports customizing default behavior through a configuration file located at `~/.soundforge/config.yaml`.

```yaml
# ~/.soundforge/config.yaml
default:
  output_format: mp3
  bitrate: 320k
  sample_rate: 44100
  channels: 2

visualize:
  width: 100
  height: 25
  color: true

batch:
  recursive: false
  overwrite: false
  parallel_jobs: 4
```

### 4.12 Typical Use Cases

**Use Case 1: Podcast Post-Production**

```bash
# 1. Check recording info
soundforge info podcast_raw.wav

# 2. Normalize volume
soundforge normalize podcast_raw.wav -o podcast_normalized.wav

# 3. Apply fade in/out
soundforge fade podcast_normalized.wav -o podcast_final.wav --fade-in 1 --fade-out 2

# 4. Convert to MP3 for publishing
soundforge convert podcast_final.wav -o podcast.mp3 --bitrate 128k
```

**Use Case 2: Music Library Organization**

```bash
# Batch convert FLAC to MP3 (save space)
soundforge batch convert ./flac_library/ --format mp3 --bitrate 320k

# Batch normalize volume
soundforge batch normalize ./mp3_library/ -o ./normalized/
```

**Use Case 3: Audio Sampling and Analysis**

```bash
# Visualize waveform
soundforge visualize sample.wav --width 120

# View spectrum
soundforge visualize sample.wav --type spectrum

# Export detailed info as JSON
soundforge info sample.wav --json > metadata.json
```

---

## 5. 💡 Design Philosophy & Roadmap

### Design Philosophy

SoundForge follows three core design principles:

1. **Simplicity first**: Each subcommand does one thing well. Parameter names are intuitive, keeping the learning curve minimal.
2. **Zero-dependency priority**: Core features are built on the Python standard library, ensuring the tool runs in any environment.
3. **Terminal aesthetics**: Colored output, progress bars, and ASCII visualizations make CLI tools a pleasure to use.

### Why Python Standard Library First?

- **Easy installation**: No need to install system-level dependencies like ffmpeg or sox, lowering the barrier to entry
- **Portability**: Pure Python implementation ensures consistent behavior across all platforms
- **Reliability**: No dependency on external tool versions, avoiding compatibility issues
- **Optional extensions**: For scenarios requiring advanced codecs, an optional ffmpeg backend is supported

### Roadmap

| Phase | Content | Status |
|-------|---------|--------|
| v1.0 | Core features: format conversion, audio editing, visualization | ✅ Done |
| v1.5 | Batch processing engine, configuration system | ✅ Done |
| v2.0 | Plugin system, enhanced recording | 🔨 In Progress |
| v2.5 | More formats (Opus, WMA), AI noise reduction | 📋 Planned |
| v3.0 | WebUI interface, remote processing mode | 📋 Planned |

---

## 6. 📦 Packaging & Deployment

### Install from PyPI

```bash
pip install soundforge
```

### Install from Source

```bash
git clone https://github.com/yourusername/soundforge.git
cd soundforge
python -m pip install -e .
```

### Using Docker

```bash
# Pull the image
docker pull soundforge/cli:latest

# Run a container
docker run --rm -v $(pwd):/data soundforge/cli info /data/audio.wav

# Batch processing
docker run --rm -v $(pwd):/data soundforge/cli batch convert /data/music/ --format mp3
```

### CI/CD Integration

**GitHub Actions Example:**

```yaml
name: Audio Processing
on: [push, pull_request]

jobs:
  process-audio:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install SoundForge
        run: pip install soundforge

      - name: Process audio files
        run: |
          soundforge batch convert ./audio/ --format mp3
          soundforge batch normalize ./audio/ -o ./output/
```

---

## 7. 🤝 Contributing

We welcome and appreciate contributions of all kinds — whether it's filing bug reports, improving documentation, or contributing code.

### Submitting a Pull Request

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add some feature"`
4. Push the branch: `git push origin feature/your-feature-name`
5. Open a **Pull Request**

**Commit message convention:** Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test-related changes
- `chore:` Build/toolchain changes

### Filing an Issue

- Use a clear and descriptive title
- Include complete steps to reproduce the issue
- Provide your environment details (OS, Python version, SoundForge version)
- If possible, attach a sample audio file

### Development Setup

```bash
git clone https://github.com/yourusername/soundforge.git
cd soundforge
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black src/ tests/
ruff check src/ tests/
```

---

## 8. 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

```
MIT License

Copyright (c) 2024 SoundForge Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**Made with ❤️ by the SoundForge Contributors**

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>
