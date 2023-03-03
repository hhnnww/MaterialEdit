from pathlib import Path
import yaml


def open_yml() -> dict:
    yml_path = Path(__file__).parent / 'replace_ad_name.yml'
    yml_text = yml_path.read_text(encoding='utf-8')

    yml = yaml.load(yml_text, Loader=yaml.FullLoader)
    return yml


if __name__ == '__main__':
    print(open_yml().get('ad_replace_keywords'))
