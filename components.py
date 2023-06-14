"""
转换的规则参考了：https://markdown.com.cn/
"""

import re

__all__ = ['Title', 'Paragraph', 'Block']


class Title:
    pattern = re.compile('(?P<level>#{1,6}) (?P<content>.*)')
    def __init__(self, source) -> None:
        self.source = source
        self.match = re.match(self.pattern, source)
    def __bool__(self) -> bool:
        return bool(self.match)
    def __str__(self) -> str:
        """调用此方法必须匹配成功，否则报错"""
        assert bool(self.match), '匹配失败'
        d = self.match.groupdict()
        level = len(d.get('level'))
        content = d.get('content')
        return f"<h{level}>{content}</h{level}>"

class Paragraph(Title):
    pattern = '.*'
    @staticmethod
    def emphasize(label, matched):
        if label == 'a':
            d = matched.groupdict()
            href = d.get('href', '')
            title = d.get('title', '')
            text = d.get('text', '') or href
            return f'<a href="{href}" title="{title}">{text}</a>'
        elif label == 'img':
            d = matched.groupdict()
            src = d.get('src', '')
            title = d.get('title', '')
            alt = d.get('alt', '') or src
            return f'<figure><img src="{src}" title="{title}" alt="{alt}" class="center">'\
                f'<figcaption class="text-align:center;">{alt}</figcaption></figure>'
        elif label == 'code':
            return f'<code class="nohighlight">{matched.group("content")}</code>'
        else:
            return f'<{label}>{matched.group("content")}</{label}>'
    def __str__(self) -> str:
        s = self.source
        for label, pattern in [
            # 以下的组件匹配存在优先级，顺序不可随意改变
            ('a', '<(?P<href>.*?)>'),
            ('del', '\~(?P<content>.*?)\~'),
            ('code', '`(?P<content>.*?)`'),
            ('img', '!\[(?P<alt>.*?)\]\((?P<src>.*?) "(?P<title>.*?)"\)'),
            ('a', '\[(?P<text>.*?)\]\((?P<href>.*?) "(?P<title>.*?)"\)'),
            ('strong', '\*\*(?P<content>.*?)\*\*'),
            ('em', '\*(?P<content>.*?)\*'),
            ]:
            s = re.sub(pattern, lambda matched:self.emphasize(label, matched), s)
        return s

class Block(Title):
    pattern = re.compile('(?P<math>\$\$\n)|(?P<code>```(?P<language>..*?)\n)')
    content = []
    def __init__(self, source) -> None:
        super().__init__(source)
        if self.match:
            self.language = self.match.groupdict().get('language')
            self.code = self.match.groupdict().get('code')
            if self.code:
                self.mark = '```\n'
            else:
                self.mark = '$$\n'
    def __str__(self) -> str:
        if self.code:
            return f'<pre><code class="language-{self.language}">' + ''.join(self.content) + '</code></pre>'
        else:
            return '$$' + ''.join(self.content) + '$$'
