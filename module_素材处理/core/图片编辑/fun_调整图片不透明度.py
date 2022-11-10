from PIL import Image


def fun_图片添加不透明度(img: Image.Image, factor: float = 0.7) -> Image.Image:
    for x in range(img.width):
        for y in range(img.height):
            color = list(img.getpixel((x, y)))
            color[-1] = int(color[-1] * factor)
            img.putpixel((x, y), tuple(color))

    return img
