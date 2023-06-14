from components import *

def parser(lines:list):
    with open('./template.html', encoding='utf8') as f:
        TEMPLATE = f.read()
    parsed = ''
    # 跨行结束的标志文本
    BLOCK_MARK = ''
    # 跨行开始的标志
    BLOCK_FLAG = False
    res = None
    for line in lines:
        if line == '\n':
            parsed += '\n<br>\n'
            continue
        # 处理跨行的代码块
        if BLOCK_FLAG and (line != BLOCK_MARK):
            res.content.append(line)
            continue
        elif line == BLOCK_MARK:
            parsed += str(res)
            # 重新开始计数
            Block.content = []
            BLOCK_FLAG = False
            continue
        else:
            pass
        for component in [Title, Block]:
            res = component(line)
            if res:
                if component is Block:
                    BLOCK_MARK = res.mark
                    BLOCK_FLAG = True
                    break
                else:
                    parsed += str(res)
                    break
        else:
            parsed += f'<p>{Paragraph(line)}</p>'
    return TEMPLATE.replace('TBD', parsed)

if __name__ == "__main__":
    with open('./source.md', mode='r', encoding='utf8') as f:
        parsed = parser(f.readlines())
    with open('./index.html', mode='w+', encoding='utf8') as f:
        f.write(parsed)