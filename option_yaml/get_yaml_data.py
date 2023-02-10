import yaml
import os

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'SeverIp.yaml'))


def read_yaml_data():
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load_all(f)
        for i in data:
            return i


if __name__ == '__main__':
    a = read_yaml_data()
    print(a)
