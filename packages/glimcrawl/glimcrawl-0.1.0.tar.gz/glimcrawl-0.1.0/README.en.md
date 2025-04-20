# GlimCrawl

[![PyPI version](https://img.shields.io/pypi/v/glimcrawl.svg)](https://pypi.org/project/glimcrawl/)
[![Python Version](https://img.shields.io/pypi/pyversions/glimcrawl.svg)](https://pypi.org/project/glimcrawl/)
[![License](https://img.shields.io/pypi/l/glimcrawl.svg)](https://gitee.com/duckweeds7/glimcrawl/blob/master/LICENSE)

English | [简体中文](README.md)

A powerful Google image crawler that supports batch downloading, image processing, and proxy settings. The name comes from "glimpse" + "crawl", emphasizing "quickly capturing web image snippets".

## ✨ Features

- 🚀 Asynchronous concurrent downloads for high efficiency
- 🎨 Automatic image processing and optimization (watermark removal, resizing, etc.)
- 🌐 Proxy support for network issues
- 📏 Image size and date filtering
- 🖥️ Easy-to-use command-line interface
- 📦 Can be used as a Python library
- 🔒 Safe and reliable, follows Google search guidelines

## 📦 Installation

```bash
# Install from PyPI (recommended)
pip install glimcrawl

# Install Playwright browser (required)
playwright install chromium
```

## 🚀 Quick Start

### Command Line Usage

```bash
# Basic usage
glimcrawl download "cats"

# Specify download count and save directory
glimcrawl download "cats" -n 50 -d ./images

# Use proxy
glimcrawl download "cats" -p http://127.0.0.1:1080

# Filter large and recent images
glimcrawl download "cats" -s l -t w
```

### Python Library Usage

```python
import asyncio
from glimcrawl import GoogleImageCrawler
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        crawler = GoogleImageCrawler(browser)
        # Download 20 cat images to images directory
        await crawler.crawl_images("cats", max_images=20, save_dir="images")
        await browser.close()

asyncio.run(main())
```

## 📝 Parameters

### Command Line Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `keyword` | Search keyword (required) | - | `"cats"` |
| `-n, --max-images` | Maximum download count | 20 | `-n 50` |
| `-d, --save-dir` | Save directory | downloaded_images | `-d ./images` |
| `-p, --proxy` | Proxy server | None | `-p http://127.0.0.1:1080` |
| `-s, --size` | Image size | None | `-s l` (large) |
| `-t, --date` | Time range | None | `-t w` (within week) |

### Image Size Options

- `l`: Large
- `m`: Medium
- `i`: Icon

### Time Range Options

- `d`: Last 24 hours
- `w`: Last week
- `m`: Last month
- `y`: Last year

## 🛠️ Image Processing

Downloaded images are automatically processed with:

1. Format conversion: Unified to JPG format
2. Size adjustment: Max 1920x1080, maintaining aspect ratio
3. Quality optimization: 85% compression rate
4. File naming: Using MD5 hash to avoid duplicates
5. Watermark removal: Automatic detection and removal (experimental)

## 🔒 Security Recommendations

1. Use HTTPS proxy when configuring proxy settings
2. Follow target website's crawler guidelines
3. Set reasonable download intervals and concurrency
4. Use images for learning and research purposes only

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feat/new-feature`
3. Commit changes: `git commit -am 'feat: add new feature'`
4. Push branch: `git push origin feat/new-feature`
5. Submit Pull Request

## 📄 License

[MIT License](LICENSE) © 2024 Duckweeds7

#### Gitee Feature

1.  You can use Readme\_XXX.md to support different languages, such as Readme\_en.md, Readme\_zh.md
2.  Gitee blog [blog.gitee.com](https://blog.gitee.com)
3.  Explore open source project [https://gitee.com/explore](https://gitee.com/explore)
4.  The most valuable open source project [GVP](https://gitee.com/gvp)
5.  The manual of Gitee [https://gitee.com/help](https://gitee.com/help)
6.  The most popular members  [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
