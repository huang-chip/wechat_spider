# 微信公众号文章爬取与AI处理工具

一个用于爬取微信公众号文章并通过 AI 处理转换为规范 Markdown 格式的工具。

## 工作流程

### 1. 爬虫部分：获取文章元素
使用爬虫从微信公众号文章中提取所有节点元素：
- 文本内容
- 图片资源
- 段落结构
- 关联书籍链接

实现代码：
```
source venv/bin/activate
```


```python
python
class WeixinSpider:
def get_article_content(self, url):
# 获取文章内容
# 提取所有元素
# 返回结构化数据
```

### 2. AI处理：内容优化与格式化
使用 AI 模型处理文章内容，主要完成：
- 错字纠正
- 标点规范化
- 常见问题修正
- 转换为 Markdown 格式

#### 2.1 图片处理
a. 段落标题图片转换
- 识别作为标题的图片
- 提取图片中的文字
- 转换为 Markdown 标题格式

b. 图片压缩处理
- 下载原始图片
- 压缩图片到 300kb 以下
- 保持图片质量

实现代码：
```python
class ImageProcessor:
def compress_image(self, image_path):
# 压缩图片逻辑
# 确保大小不超过 300kb
```


---
# 讨论结果
最后暴露出一个接口，或者涉及到ai的部份，用dify的接口进行任务处理。
用到AI的部份：修改错别字，格式化，删除不必要的字

## 分工
问AI要prompt，带入到文本中进行效果检验，每一次的对话后，得到一个满意的prompt