# 从html中获取组成png图像。把图像塞到对应人物的文件夹里。
html_path = "/Users/jyxc0100522/code/部队 - 苏丹的游戏WIKI_BWIKI_哔哩哔哩.html"
save_path = "/Users/jyxc0100522/code/sultan_card_images/armies/"
file_path = "/Users/jyxc0100522/code/部队 - 苏丹的游戏WIKI_BWIKI_哔哩哔哩_files"

# import beautifulsoup
# pip install beautifulsoup4
from bs4 import BeautifulSoup
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
# open html file
file = open(html_path, "r")
html = file.read()
file.close()

# parse html
soup = BeautifulSoup(html, "html.parser")

# 找div CardSelectTr
card_select_tr = soup.find("div", id="CardSelectTr")

# 找div CardSelectTr下的所有divsort，每个divsort是一个卡牌
div_sorts = card_select_tr.find_all("div", class_="divsort")

count_name = {}
# 对于每一个卡牌
for div_sort in div_sorts:
    try:
        name = div_sort.find("div", class_="card-name")
        name = name.text
        print(name)
        
        # 找ping0
        ping = div_sort.find("div", class_="ping0")
        all_images = []
        # 获取里面所有的a href
        a_tags = ping.find_all("a")
        # 获取a标签的href
        for a_tag in a_tags:
            # <a href="https://wiki.biligame.com/sultansgame/%E6%96%87%E4%BB%B6:%E9%87%91%E5%BA%95-%E8%8A%B1%E7%BA%B9.png" class="image"><img alt="金底-花纹.png" src="./characters_files/pe9pxsozbha9i4obfkvfwrtdo7zecvz.png" decoding="async" loading="lazy" width="194" height="422" data-file-width="194" data-file-height="422"></a>
            # 获取src
            src = a_tag.find("img").get("src")
            # 获取src的文件名
            file_name = src.split("/")[-1]
            all_images.append(file_name)
        # print(all_images)
        if name in count_name:
            count_name[name] += 1
            tmp_save_dir = os.path.join(save_path, name + "_" + str(count_name[name]))
        else:
            count_name[name] = 1
            tmp_save_dir = os.path.join(save_path, name)
        
        if not os.path.exists(tmp_save_dir):
            os.makedirs(tmp_save_dir)
        for i, image in enumerate(all_images):
            new_image_path = os.path.join(tmp_save_dir, f"{i}.png")
            # copy image to new_image_path
            shutil.copy(os.path.join(file_path, image), new_image_path)
    except Exception as e:
        print(e)
        print("跳过:", name)
        continue


# 把每个character的图片合成到一个png里。resize短边之后居中放置。
for name in os.listdir(save_path):
    tmp_save_dir = os.path.join(save_path, name)
    all_images = os.listdir(tmp_save_dir)
    # sort by name
    all_images.sort(key=lambda x: int(x.split(".")[0]))
    # pillow 读取
    images = []
    for image in all_images:
        # 打开带Alpha通道的图片
        image = Image.open(os.path.join(tmp_save_dir, image)).convert("RGBA") # 所有人物图片都是472*1028的
        images.append(image)
    # resize 每一个图片
    for idx in range(len(images)):
        images[idx] = images[idx].resize((472, int(images[idx].size[1] * 472 / images[idx].size[0])))
    # 合成图片，图片尺寸为第一张图的尺寸
    new_image = Image.new("RGBA", (images[0].size[0], images[0].size[1]))
    for image in images:
        # 忽略Alpha通道
        new_image.paste(image, (0, 0), image)
    # 保存
    new_image.save(os.path.join(save_path, name, "merged.png"))

# 添加文本
card_width = 472
card_height = 1028
font_size = int(card_width * 29/130)
font_path = "/Users/jyxc0100522/Downloads/汉仪杰龙桃花源.ttf"
font = ImageFont.truetype(font_path, font_size)

for name in os.listdir(save_path):
    image_path = os.path.join(save_path, name, "merged.png")
    img = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    text = name.split("_")[0]
    if text == "主角":
        text = "阿尔图"
    # 计算位置
    y_position = card_height * 0.03
    max_width = 472 - int(472*10/130)
    # 文本换行
    lines = []
    for line in text.split('\n'):
        wrapped = textwrap.wrap(line, width=4)  # 每行最多4个汉字
        lines.extend(wrapped)
    # 绘制文本（带阴影效果）
    line_height = int(font_size * 0.9) # 行高
    for line in lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:4]
        x = (card_width - text_width) / 2
        shadow_offset = int(font_size * 0.05)
        # 绘制阴影
        if name != "苏丹":
            # 阴影
            # draw.text((x+shadow_offset, y_position+shadow_offset), 
                # line, font=font, fill="#ffffff")
            # 绘制主文本
            # draw.text((x, y_position), line, font=font, fill="#000000")
            # --- 替换你原有代码的完整部分 ---

            # 1. 创建一个**临时**的透明图像，专门用于绘制阴影。
            # 阴影必须绘制到独立的层上才能被模糊。
            shadow_temp_image = Image.new("RGBA", img.size, (255, 255, 255, 0))

            # 2. 为这个临时图像创建一个新的 ImageDraw 对象。
            # 我们用它来在 shadow_temp_image 上绘制阴影。
            shadow_draw_temp = ImageDraw.Draw(shadow_temp_image)

            # 3. 在临时阴影图像上绘制**白色**的文本（这将是你的阴影）。
            shadow_draw_temp.text((x + shadow_offset, y_position + shadow_offset),
                                line, font=font, fill="#FFFFFF") # fill="#FFFFFF" 表示白色阴影

            # 4. 对这个临时阴影图像应用高斯模糊。
            blur_radius = 5
            blurred_shadow_image = shadow_temp_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

            # 5. 将模糊后的阴影图像合成到你的**主图像** (`base_image`) 上。
            # `base_image` 就是你的 `draw` 对象所操作的图像。
            img.alpha_composite(blurred_shadow_image)

            # 6. 最后，使用你**原有**的 `draw` 对象在主图像上绘制**黑色**的文本。
            # 这是你代码中“绘制主文本”的部分。
            draw.text((x, y_position), line, font=font, fill="#000000") # fill="#000000" 表示黑色文本

            # --- 代码替换结束 ---
            y_position += line_height
        else:
            # 没有阴影。绘制主文本
            draw.text((x, y_position), line, font=font, fill="#f2e78f")
            y_position += line_height
    
    new_path = os.path.join(save_path, name, "merged_with_text.png")
    img.save(new_path)

"""
wiki中的图片的样式表：
.card-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin:8px 4px;
  width:130px;
}
文本的样式表：
.card-name {
  position: absolute;
  text-align: center;
  text-shadow: 0.05em 0.05em 0.1em #fff;
  top: 5%;
  font-family: 汉仪杰龙桃花源;
  color: #000;
  font-size: clamp(5px,2.1em,2.1em);
  width: 100%;
  line-height: 0.9em;
}
.sudan-name {
  color: #f2e78f;
  text-shadow: unset;
}
"""