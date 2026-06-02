# 本地文字实时翻译

一个基于Ollama和Qwen3-VL模型的本地实时文字翻译工具。你不需要网上付费进行翻译，也不必担心隐私泄露问题，而你唯一需要做的就是配置本地模型接着尽情使用！
使用演示视频教程地址: https://www.bilibili.com/video/BV1DDV66qEko/?share_source=copy_web&vd_source=d33f40c80ac747e9389492765ef14959

## 功能特点

- 🚀 **本地运行**：所有翻译在本地完成，无需联网，保护隐私
- 📸 **截图翻译**：支持截图区域选择，实时识别并翻译图片中的文字
- 🌐 **多语言支持**：基于Qwen3-VL多模态模型，支持多种语言识别和翻译
- 🖥️ **简洁界面**：轻量级GUI界面，操作简单直观

## 系统要求

- Windows 10/11 (64位)
- Python 3.8+
- 至少8GB内存（推荐16GB以上）
- 支持CUDA的NVIDIA GPU（推荐，可加快推理速度）

## 安装步骤

### 第一步：安装Ollama

1. 访问 Ollama 官方网站：[https://ollama.com/](https://ollama.com/)
2. 下载对应系统的安装包（Windows版本）
3. 运行安装程序，按照提示完成安装
4. 安装完成后，打开命令提示符（CMD）或PowerShell，验证安装：
   ```bash
   ollama --version
   ```

### 第二步：拉取Qwen3-VL模型

打开命令提示符或PowerShell，执行以下命令下载模型：

```bash
ollama pull adelnazmy2002/Qwen3-VL-4B-Instruct:Q4_K_M
```

> ⚠️ **注意**：模型文件较大（约5GB左右），请确保有足够的存储空间和稳定的网络连接。

### 第三步：安装Python依赖

如果使用源代码运行，需要安装以下依赖：

```bash
pip install langchain-core langchain-ollama pillow
```

## 使用方法

### 方法一：直接运行可执行文件（推荐）

1. 确保已经完成**第一步**和**第二步**的安装
2. 双击运行 `translate.exe`
3. 点击「设置翻译区域」按钮，用鼠标框选需要翻译的屏幕区域
4. 点击「启动翻译」按钮开始实时翻译

### 方法二：运行Python脚本

```bash
python translate-requests.py
```

### 操作说明

1. **设置翻译区域**：点击按钮后，屏幕会出现半透明遮罩，用鼠标拖拽选择要监控的区域（最小32x32像素）
2. **启动翻译**：点击按钮开始实时翻译，每秒截图并识别区域内的文字
3. **停止翻译**：再次点击「启动翻译」按钮停止翻译
4. **按Esc退出区域选择**：在选择区域时按Esc键可取消选择

## 项目结构

```
├── README.md          # 项目说明文档
├── translate.exe      # Windows可执行文件
└── translate-requests.py  # Python源代码
```

## 技术栈

- **框架**: Tkinter (GUI)
- **LLM框架**: LangChain
- **模型**: Qwen3-VL-4B-Instruct (Ollama)
- **图片处理**: Pillow

## 注意事项

1. 首次运行需要加载模型，可能需要等待几秒钟
2. 翻译区域不宜过大，建议只框选需要翻译的文字区域
3. 翻译结果显示有字数限制，过长的文本可能无法完全显示
4. 确保Ollama服务正在运行（启动时会自动运行）
5. 如果遇到错误，请尝试重新启动程序

## 常见问题

**Q: 运行时提示"请尝试重新启动"？**

A: 请检查：
- Ollama是否已正确安装
- 模型是否已成功下载（运行 `ollama list` 查看）
- 系统内存是否充足

**Q: 翻译速度很慢？**

A: 建议使用NVIDIA GPU并安装CUDA驱动，可显著提升推理速度。

**Q: 模型下载失败？**

A: 可以尝试更换网络环境，或使用代理下载。

## License

MIT License
