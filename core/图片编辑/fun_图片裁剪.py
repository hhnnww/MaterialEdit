from PIL import Image


def fun_图片裁剪(im: Image.Image, width: int, height: int) -> Image.Image:
    im_ratio = im.width / im.height
    ori_ratio = width / height

    if im_ratio > ori_ratio:
        height_ratio = im.height / height
        ori_width = int(im.width / height_ratio)
        im = im.resize((ori_width, height), resample=Image.ANTIALIAS)
        left = int((ori_width - width) / 2)
        im = im.crop((left, 0, left + width, height))

    elif im.width / im.height < width / height:
        width_ratio = im.width / width
        ori_height = int(im.height / width_ratio)
        im = im.resize((width, ori_height), resample=Image.ANTIALIAS)
        top = int(
            (ori_height - height) / 2
        )
        im = im.crop((0, top, width, top + height))

    else:
        im = im.resize((width, height))

    return im


if __name__ == '__main__':
    img = Image.open(r'E:\小夕素材\8000-8999\8215\8215\小夕素材(1).png')
    img = fun_图片裁剪(img, 1200, 500)
    print(img.size)
    img.show()
