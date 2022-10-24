import re
from pathlib import Path


def fun_获取数字(file_path: Path) -> int:
    num_list = re.findall('\d+', file_path.stem)
    if len(num_list) == 0:
        return 0

    num = ''.join(num_list)
    num = int(num)

    return num


if __name__ == '__main__':
    n = fun_获取数字(
        Path(r'E:\DOWN\cute-cat-logo-mascot\sadf.eps')
    )
    print(n)
