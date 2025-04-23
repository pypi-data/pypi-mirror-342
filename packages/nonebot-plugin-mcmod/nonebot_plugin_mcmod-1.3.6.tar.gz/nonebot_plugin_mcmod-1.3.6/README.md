<h1 align="center"> nonebot-plugin-mcmod </h1>

<p align="center">
  <a href="https://github.com/chrysoljq/nonebot-plugin-mcmod">
    <img src="https://img.shields.io/github/license/chrysoljq/nonebot-plugin-mcmod" alt="LICENSE">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot_plugin_mcmod">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_mcmod" alt="PyPI">
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.3.0+-red" alt="NoneBot">
  </a>
</p>

<p align="center">
  基于 NoneBot2 的 模组百科 (MCMOD) 查询插件
</p>

## 📖 介绍

一个简单的 NoneBot2 插件，用于在 https://www.mcmod.cn (我的世界百科) 搜索模组、整合包、教程和资料等信息。

通过指令在 QQ 群从查询 Minecraft 中文模组百科相关内容。以转发消息的形式展示搜索信息，目前支持搜索、标题、正文文本和图片内容获取。

![示例](img/image.png)

## 💿 安装
**使用 git:**
```bash
git clone https://github.com/chrysoljq/nonebot-plugin-mcmod
```
然后将 `nonebot-plugin-mcmod/nonebot_plugin_mcmod` 复制到你的插件目录下。

**使用 pip:**

```bash
pip install nonebot_plugin_mcmod
```

**使用 nb-cli:**

```bash
nb plugin install nonebot_plugin_mcmod
```

安装后，请在你的 `bot.py` 或 `pyproject.toml` 中加载插件：

```python
# bot.py
nonebot.load_plugin("nonebot_plugin_mcmod")
```

```toml
# pyproject.toml
[tool.nonebot]
plugins = ["nonebot_plugin_mcmod"]
```

## 🚀 使用

**指令格式:**

```
#百科[分类] <关键词> [序号]
```
若无序号，则会等待用户下一次数字输入

**参数说明:**

  * `[分类]`: 可选参数，用于指定搜索范围。可选值为 `整合包`, `模组`, `教程`, `资料`。如果省略，则在所有分类中搜索。
  * `<关键词>`: 必填参数，你要搜索的内容。可以包含空格。
  * `[序号]`: 可选参数，当搜索结果多于一个时，可以通过序号选择查看特定结果的详细信息（序号从 1 开始）。

**示例:**

  * `#百科模组 工业` - 搜索分类为“模组”，关键词为“工业”的内容。
  * `#百科整合包 石头世界` - 搜索分类为“整合包”，关键词为“石头世界”的内容。
  * `#百科 巫妖 恐怖生物` - 在所有分类中搜索关键词为“巫妖 恐怖生物”的内容。
  * `#百科 暮色森林 2` - 查看“暮色森林”搜索结果中的第 2 条详细信息。

## 📝 TODO

  * [x] 获取整合包/模组支持的 Minecraft 版本信息。
  * [x] 完善搜索结果中的图片爬取与展示。
  * [ ] 增加配置项，例如结果数量限制等。
  * [ ] 为对话流程添加超时机制
  * [ ] 控制消息长度

## 🙏 致谢

  * [mcmod.cn](https://www.mcmod.cn/) - 提供数据来源。
  * [nonebot2](https://github.com/nonebot/nonebot2) - 插件开发框架。
  * [Gemini](https://gemini.google.com/app) - 代码助手，大大加快开发流程。
  * [limbang/mirai-console-mcmod-plugin](https://github.com/limbang/mirai-console-mcmod-plugin) - 提供灵感来源。

## 📄 开源许可

本项目使用 [MIT License](https://www.google.com/search?q=LICENSE) 开源。

