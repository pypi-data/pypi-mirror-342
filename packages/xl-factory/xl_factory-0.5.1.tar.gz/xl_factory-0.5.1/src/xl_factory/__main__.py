import os
import sys
import importlib.util
from pathlib import Path
import yaml
from sqlalchemy import text


def find_file_upwards(start_path: Path, target_file: str) -> Path:
    current_path = start_path
    while current_path != current_path.parent:
        target_path = current_path / target_file
        if target_path.exists():
            return target_path
        current_path = current_path.parent
    return None


def import_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


start_directory = Path.cwd() # 从当前命令行执行路径开始
target_file = 'factory.py'
factory_path = find_file_upwards(start_directory, target_file)
if factory_path:
    # Add factory.py's directory to sys.path
    factory_dir = str(factory_path.parent)
    if factory_dir not in sys.path:
        sys.path.append(factory_dir)
    factory_module = import_module_from_path('factory', str(factory_path))
    factory = getattr(factory_module, 'factory')
else:
    print(f"{target_file} not found.")


if len(sys.argv) < 1:
    print("Usage: python script.py <module_name>")
    sys.exit(1)


module_name = sys.argv[1]
if module_name == 'data':
    yaml_path = Path('data.yaml')
    with yaml_path.open(encoding='utf-8') as f:
        table_config = yaml.safe_load(f)
        table_name = table_config.get('table', '')
        table_comment = table_config.get('chinese', '')
        table_columns = table_config.get('columns', [])
        engine = factory.create_engine()
        with engine.connect() as conn:
            if table_comment:
                conn.execute(
                    text(f"ALTER TABLE {table_name} COMMENT ='{table_comment}'")
                )
            for table_column in table_columns:
                column_name = table_column.get('prop', '')
                column_comment = table_column.get('label', '')
                if column_comment:
                    result = conn.execute(text(f"SHOW FULL COLUMNS FROM {table_name} WHERE Field = '{column_name}'"))
                    column_info = result.fetchone()
                    if column_info:
                        column_type = column_info[1]
                        is_nullable = "NULL" if column_info[3] == "YES" else "NOT NULL"

                        # 构建 ALTER TABLE 语句
                        sql = f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {column_type} {is_nullable} COMMENT '{column_comment}'"

                        conn.execute(text(sql))

else:
    factory.make_module(module_name)
