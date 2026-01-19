import os
import requests
from bs4 import BeautifulSoup
import json
import re

# 1. 这里是你提供的 HTML 数据
html_content = """
<table class="table-ShipWordsTable" data-title="白兔迎春">
<tbody><tr data-key="desc">
<th>皮肤描述</th>
<td><div class="ship_word_block ship_word_media_wrap" data-key="desc" data-key-i="1">
<p class="ship_word_line" data-lang="zh" data-key="desc" data-key-i="1">
…新年快乐，吉祥如意？这么说就可以了…？唔，感觉有点困了，拉菲可以回去再睡会了吗？ </p>
<div class="sm-bar" style="display: block;"><span title="获取" class="sm-button sm-play-pause"></span><div class="sm-audio-src"><a rel="nofollow" class="external free" href="https://patchwiki.biligame.com/images/blhx/0/09/kv55gsssuoyy86fyfjop6dhjd05fh5j.mp3">https://patchwiki.biligame.com/images/blhx/0/09/kv55gsssuoyy86fyfjop6dhjd05fh5j.mp3</a></div></div></div></td>
</tr>
<tr data-key="login">
<th>登录台词</th>
<td><div class="ship_word_block ship_word_media_wrap" data-key="login" data-key-i="1">
<p class="ship_word_line" data-lang="zh" data-key="login" data-key-i="1">
指挥官还不回来，拉菲要靠着树睡着了……Zzz…… </p>
<div class="sm-bar" style="display: block;"><span title="登录" class="sm-button sm-play-pause"></span><div class="sm-audio-src"><a rel="nofollow" class="external free" href="https://patchwiki.biligame.com/images/blhx/2/26/pj8x0zig6sssgt423mzmu5g1tuc8mp2.mp3">https://patchwiki.biligame.com/images/blhx/2/26/pj8x0zig6sssgt423mzmu5g1tuc8mp2.mp3</a></div></div></div></td>
</tr>
<tr data-key="detail">
<th>查看详情</th>
<td><div class="ship_word_block ship_word_media_wrap" data-key="detail" data-key-i="1">
<p class="ship_word_line" data-lang="zh" data-key="detail" data-key-i="1">
新年…春节…有什么不同吗？拉菲不是很明白…不过，能好吃好睡的节日…就是好节日，嗯 </p>
<div class="sm-bar" style="display: block;"><span title="查看详情" class="sm-button sm-play-pause"></span><div class="sm-audio-src"><a rel="nofollow" class="external free" href="https://patchwiki.biligame.com/images/blhx/9/94/f4xfy112noh5lfcz15ah1qa4bwk3hoq.mp3">https://patchwiki.biligame.com/images/blhx/9/94/f4xfy112noh5lfcz15ah1qa4bwk3hoq.mp3</a></div></div></div></td>
</tr>
<tr data-key="main">
<th>主界面</th>
<td><div class="ship_word_block ship_word_media_wrap" data-key="main" data-key-i="1">
<p class="ship_word_line" data-lang="zh" data-key="main" data-key-i="1">
春节限定版兔耳和兔兔拖鞋…指挥官喜欢吗？拉菲…很喜欢… </p>
<div class="sm-bar" style="display: block;"><span title="主界面_1" class="sm-button sm-play-pause"></span><div class="sm-audio-src"><a rel="nofollow" class="external free" href="https://patchwiki.biligame.com/images/blhx/7/71/d12vav44ouhaktcc4zw9y4w4cpwnb3h.mp3">https://patchwiki.biligame.com/images/blhx/7/71/d12vav44ouhaktcc4zw9y4w4cpwnb3h.mp3</a></div></div></div><div class="ship_word_block ship_word_media_wrap" data-key="main" data-key-i="2">
<p class="ship_word_line" data-lang="zh" data-key="main" data-key-i="2">
z23，好像对春节的传说很有兴趣的样子…… </p>
<div class="sm-bar" style="display: block;"><span title="主界面_2" class="sm-button sm-play-pause"></span><div class="sm-audio-src"><a rel="nofollow" class="external free" href="https://patchwiki.biligame.com/images/blhx/e/e1/hvlmlx0y3fxg7ezhblq9n73bypj8ic5.mp3">https://patchwiki.biligame.com/images/blhx/e/e1/hvlmlx0y3fxg7ezhblq9n73bypj8ic5.mp3</a></div></div></div><div class="ship_word_block ship_word_media_wrap" data-key="main" data-key-i="3">
<p class="ship_word_line" data-lang="zh" data-key="main" data-key-i="3">
像这样在树上坐着，拉菲感觉自己也要开花了… </p>
<div class="sm-bar" style="display: block;"><span title="主界面_3" class="sm-button sm-play-pause"></span><div class="sm-audio-src"><a rel="nofollow" class="external free" href="https://patchwiki.biligame.com/images/blhx/a/a8/58nl6vehfa6n1ypmgf25pvvhvjr6w6b.mp3">https://patchwiki.biligame.com/images/blhx/a/a8/58nl6vehfa6n1ypmgf25pvvhvjr6w6b.mp3</a></div></div></div></td>
</tr>
<tr data-key="touch">
<th>触摸台词</th>
<td><div class="ship_word_block ship_word_media_wrap" data-key="touch" data-key-i="1">
<p class="ship_word_line" data-lang="zh" data-key="touch" data-key-i="1">
拉菲没有想借指挥官的肩膀靠一会，嗯，并没有…… </p>
<div class="sm-bar" style="display: block;"><span title="普通触摸" class="sm-button sm-play-pause"></span><div class="sm-audio-src"><a rel="nofollow" class="external free" href="https://patchwiki.biligame.com/images/blhx/5/5d/0o79pdu6j5cdutlqtqcynpl6r9unqtj.mp3">https://patchwiki.biligame.com/images/blhx/5/5d/0o79pdu6j5cdutlqtqcynpl6r9unqtj.mp3</a></div></div></div></td>
</tr>
<tr data-key="touch2">
<th>特殊触摸</th>
<td><div class="ship_word_block ship_word_media_wrap" data-key="touch2" data-key-i="1">
<p class="ship_word_line" data-lang="zh" data-key="touch2" data-key-i="1">
<span class="heimu" title="">指挥官，又在想奇怪的事了吗…</span> </p>
<div class="sm-bar" style="display: block;"><span title="特殊触摸" class="sm-button sm-play-pause"></span><div class="sm-audio-src"><a rel="nofollow" class="external free" href="https://patchwiki.biligame.com/images/blhx/d/db/qxa1j53req0zthw0oan00v5un646yqv.mp3">https://patchwiki.biligame.com/images/blhx/d/db/qxa1j53req0zthw0oan00v5un646yqv.mp3</a></div></div></div></td>
</tr>
<tr data-key="home">
<th>回港台词</th>
<td><div class="ship_word_block ship_word_media_wrap" data-key="home" data-key-i="1">
<p class="ship_word_line" data-lang="zh" data-key="home" data-key-i="1">
那个红红的，一串一串，烧起来之后砰砰砰砰的……唔，有点吵…… </p>
<div class="sm-bar" style="display: block;"><span title="回港" class="sm-button sm-play-pause"></span><div class="sm-audio-src"><a rel="nofollow" class="external free" href="https://patchwiki.biligame.com/images/blhx/8/87/03g291ta4dv700vpcsm8oixxy48tsio.mp3">https://patchwiki.biligame.com/images/blhx/8/87/03g291ta4dv700vpcsm8oixxy48tsio.mp3</a></div></div></div></td>
</tr>
</tbody></table>
"""

# 2. 设置保存路径
save_dir = "lafei_4/sound"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

soup = BeautifulSoup(html_content, 'html.parser')
rows = soup.find_all('tr')

voice_map = {}
download_count = 0

print(f"开始处理，将保存到 {save_dir}/ 文件夹...")

# 3. 遍历每一行数据
for tr in rows:
    key = tr.get('data-key')
    if not key:
        continue
    
    # 找到该行内所有的语音块（有的行如 main 可能有多个）
    blocks = tr.find_all(class_='ship_word_block')
    
    for block in blocks:
        # 获取文本
        text_p = block.find(class_='ship_word_line')
        text_content = text_p.text.strip() if text_p else ""
        
        # 获取音频链接
        audio_div = block.find(class_='sm-audio-src')
        if audio_div:
            a_tag = audio_div.find('a')
            if a_tag:
                url = a_tag['href']
                
                # 获取索引 (用于处理 main_1, main_2 这种情况)
                index = block.get('data-key-i')
                
                # 命名逻辑：如果有多个语音，或者索引不为1，就加上后缀
                # 这里为了稳妥，如果是主界面(main)或者索引大于1的，都加后缀
                # 你也可以改成: filename = f"{key}.mp3" if len(blocks) == 1 else f"{key}_{index}.mp3"
                if len(blocks) > 1:
                    filename = f"{key}_{index}.mp3"
                else:
                    filename = f"{key}.mp3"
                
                filepath = os.path.join(save_dir, filename)
                
                # 记录到 map 中
                voice_map[filename] = text_content
                
                # 下载文件
                try:
                    print(f"正在下载: {filename} ...")
                    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with open(filepath, 'wb') as f:
                        f.write(r.content)
                    download_count += 1
                except Exception as e:
                    print(f"下载失败 {url}: {e}")

# 4. 生成对应关系的 JSON 文件
json_path = "voice_map.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(voice_map, f, ensure_ascii=False, indent=4)

print("-" * 30)
print(f"处理完成！")
print(f"共下载音频: {download_count} 个")
print(f"语音对应表已保存为: {json_path}")
print(f"请查看文件夹: {os.path.abspath(save_dir)}")