import pymysql
import os

# 定义字段类型映射表
FIELD_TYPE_MAP = {
    'int': 'IntegerField',
    'smallint': 'SmallIntegerField',
    'varchar': 'CharField',
    'text': 'TextField',
    'datetime': 'DateTimeField',
    'date': 'DateField',
    'float': 'FloatField',
    'decimal': 'DecimalField',
}


def get_field_type(sql_type):
    """根据数据库类型获取 Django 字段类型"""
    for key, value in FIELD_TYPE_MAP.items():
        if key in sql_type.lower():
            return value
    return 'TextField'


def snake_to_camel(name):
    """将下划线命名转换为驼峰命名"""
    return ''.join(word.capitalize() for word in name.split('_'))


def generate_model_code(table_name, django_env: str):
    """根据表结构生成 Django 模型代码"""
    os.environ['DJANGO_ENV'] = django_env

    from DjangoProject import settings
    project_name = settings.PROJECT_NAME

    host = settings.DATABASES['default']['HOST']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database = settings.DATABASES['default']['NAME']

    # 连接数据库
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        charset='utf8mb4'
    )
    cursor = connection.cursor()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()

    cursor.execute(f"SHOW TABLE STATUS WHERE Name = '{table_name}'")
    table_info = cursor.fetchone()
    table_comment = table_info[-1] if table_info else ''

    class_name = snake_to_camel(table_name)
    model_code = f"from django.db import models\nfrom django.utils import timezone\n\n\nclass {class_name}(models.Model):\n"

    for column in columns:
        field_name = column[0]
        sql_type = column[1]
        is_nullable = column[2] == 'YES'
        is_primary = column[3] == 'PRI'
        default = column[4]
        comment = column[-1] if len(column) > 5 else ''

        field_type = get_field_type(sql_type)
        field_args = []

        if is_primary:
            field_type = 'AutoField' if 'int' in sql_type else field_type
            field_args.append("primary_key=True")
        elif column == 'created_at':
            field_args.append(f"default=timezone.now")
        elif column == 'updated_at':
            field_args.append(f"auto_now=True")
        elif default is not None:
            if isinstance(default, str):
                field_args.append(f"default='{default}'")
            else:
                field_args.append(f"default={default}")

        if field_type == 'CharField' and 'varchar' in sql_type:
            max_length = int(sql_type[sql_type.find('(') + 1:sql_type.find(')')])
            field_args.append(f"max_length={max_length}")
        elif field_type == 'DecimalField' and 'decimal' in sql_type:
            # 解析 max_digits 和 decimal_places
            digits_info = sql_type[sql_type.find('(') + 1:sql_type.find(')')].split(',')
            max_digits = digits_info[0].strip()
            decimal_places = digits_info[1].strip()
            field_args.append(f"max_digits={max_digits}, decimal_places={decimal_places}")

        if not is_primary and is_nullable:
            field_args.append("null=True")

        if comment:
            field_args.append(f"verbose_name='{comment}'")

        field_args_str = ", ".join(field_args)
        model_code += f"    {field_name} = models.{field_type}({field_args_str})\n"

    model_code += "\n    class Meta:\n"
    model_code += f"        db_table = '{table_name}'\n"
    if table_comment:
        model_code += f"        verbose_name = '{table_comment}'\n"
        model_code += f"        verbose_name_plural = '{table_comment}'\n"
    model_code += "        managed = False\n"

    # 关闭连接
    cursor.close()
    connection.close()

    print(model_code)

    download_dir = os.path.join(PROJECT_ROOT, f'{project_name}\\entity\\model')
    # download_dir = os.path.join(os.path.expanduser("~"), "Documents")
    # 将生成的代码保存到 Python 文件
    file_name = os.path.join(download_dir, f"{table_name.lower()}.py")

    with open(file_name, 'w', encoding="UTF-8") as model_file:
        model_file.write(model_code)
        print(f"Generated {file_name}")

        # 生成 expose 类代码
        expose_class_code = f"""from typing import Optional
from django.db import transaction
from TerminatorBaseCore.entity.exception import BusinessException
from TerminatorBaseCore.entity.response import ServiceJsonResponse
from TerminatorBaseCore.route.route import prefix, route, Method
from TerminatorBaseCore.route.viewset import CustomRouterViewSet
from TerminatorBaseCore.service.base_compoment_handler import BaseCompomentHandler
from {project_name}.entity.model.{table_name.lower()} import {class_name}


@prefix('api/{table_name}')
class {class_name}Expose(CustomRouterViewSet, BaseCompomentHandler[{class_name}]):
    pass
"""

        # 保存 expose 文件
        download_dir = os.path.join(PROJECT_ROOT, f'{project_name}\\expose')
        expose_file_name = os.path.join(download_dir, f"{table_name.lower()}_expose.py")
        with open(expose_file_name, 'w', encoding="UTF-8") as expose_file:
            expose_file.write(expose_class_code)
            print(f"Generated {expose_file_name}")

        # 生成 service 类代码
        service_class_code = f"""from typing import Optional
from {project_name}.entity.model.{table_name.lower()} import {class_name}
from TerminatorBaseCore.service.base_service_handler import BaseServiceHandler


class {class_name}Service(BaseServiceHandler[{class_name}]):
    pass
"""

        # 保存 service 文件
        download_dir = os.path.join(PROJECT_ROOT, f'{project_name}\\service')
        service_file_name = os.path.join(download_dir, f"{table_name.lower()}_service.py")
        with open(service_file_name, 'w', encoding="UTF-8") as service_file:
            service_file.write(service_class_code)
            print(f"Generated {service_file_name}")

    return model_code


if __name__ == "__main__":
    # 提示用户输入数据库配置
    # 指定表名
    generate_model_code('token_orders', 'development')
