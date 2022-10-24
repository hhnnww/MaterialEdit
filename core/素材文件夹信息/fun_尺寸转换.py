def fun_尺寸转换(st_size: float) -> str:
    size_list = ['B', 'KB', 'MB', 'GB']
    level = 0
    while st_size > 1024:
        st_size = st_size / 1024
        level += 1

    return f'{round(st_size, 2)} {size_list[level]}'


if __name__ == '__main__':
    print(fun_尺寸转换(
        12312
    ))
