import requests
from bs4 import BeautifulSoup
import markdown
import re
import time
from datetime import datetime

class WeixinArticleSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_article_content(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 获取文章标题 (使用meta标签获取更可靠)
                title = soup.find('meta', property='og:title')['content']

                # 获取文章作者
                author = soup.find('meta', property='og:article:author')['content']

                # 获取文章描述
                description = soup.find('meta', property='og:description')['content']

                # 获取文章内容
                content = soup.find('div', id='js_content')
                if not content:
                    raise Exception("无法找到文章内容")

                # 处理图片
                images = []
                img_tags = content.find_all('img')
                for img in img_tags:
                    # 获取图片真实链接
                    data_src = img.get('data-src')
                    if data_src:
                        images.append({
                            'url': data_src,
                            'alt': img.get('alt', '')
                        })
                        # 替换图片链接
                        img['src'] = data_src

                # 清理HTML标签，但保留段落结构
                article_text = self.clean_html(str(content))

                return {
                    'title': title,
                    'author': author,
                    'description': description,
                    'content': article_text,
                    'images': images
                }

            return None

        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def clean_html(self, html_content):
        """清理HTML内容，保留基本格式"""
        # 使用BeautifulSoup进行解析
        soup = BeautifulSoup(html_content, 'html.parser')

        # 删除script和style标签
        for script in soup(['script', 'style']):
            script.decompose()

        # 处理段落和换行
        for br in soup.find_all('br'):
            br.replace_with('\n')

        for p in soup.find_all('p'):
            p.append(soup.new_string('\n'))

        # 获取处理后的文本
        text = soup.get_text()

        # 清理多余的空行和空格
        lines = (line.strip() for line in text.splitlines())
        text = '\n'.join(line for line in lines if line)

        return text

    def save_to_markdown(self, data, output_file):
        if not data:
            return False

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # 写入标题
                f.write(f"# {data['title']}\n\n")

                # 写入时间戳
                f.write(f"*抓取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

                # 写入正文
                f.write(data['content'])

            return True

        except Exception as e:
            print(f"Error saving to markdown: {str(e)}")
            return False

def main():
    url = "https://mp.weixin.qq.com/s/-nlA13tKEHNL7yH3VjVMrA"
    spider = WeixinArticleSpider()

    # 获取文章内容
    article_data = spider.get_article_content(url)

    if article_data:
        print(f"标题: {article_data['title']}")
        print(f"作者: {article_data['author']}")
        print(f"描述: {article_data['description']}")
        print(f"图片数量: {len(article_data['images'])}")
        # 保存为markdown文件
        output_file = f"weixin_article_{int(time.time())}.md"
        if spider.save_to_markdown(article_data, output_file):
            print(f"文章已成功保存到 {output_file}")
        else:
            print("保存文章失败")
    else:
        print("获取文章内容失败")

if __name__ == "__main__":
    main()