import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--image_path", type=str, required=True)
parser.add_argument("--save_path", type=str, required=True)
parser.add_argument("--text", type=str, required=True)
args = parser.parse_args()

# 添加文本
card_width = 472
card_height = 1028
font_size = int(card_width * 29/130)
font_path = "汉仪杰龙桃花源.ttf"
font = ImageFont.truetype(font_path, font_size)

img = Image.open(args.image_path).convert("RGBA")
draw = ImageDraw.Draw(img)
# 计算位置
y_position = card_height * 0.03
max_width = 472 - int(472*10/130)
# 文本换行
lines = []
for line in args.text.split('\n'):
    wrapped = textwrap.wrap(line, width=4)  # 每行最多4个汉字
    lines.extend(wrapped)
# 绘制文本（带阴影效果）
line_height = int(font_size * 0.9) # 行高
for line in lines:
    text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:4]
    x = (card_width - text_width) / 2
    shadow_offset = int(font_size * 0.05)
    # 阴影
    # draw.text((x+shadow_offset, y_position+shadow_offset), 
        # line, font=font, fill="#ffffff")
    # 绘制主文本
    # draw.text((x, y_position), line, font=font, fill="#000000")

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

    y_position += line_height

new_path = os.path.join(args.save_path)
img.save(new_path)