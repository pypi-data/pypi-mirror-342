# -*- coding: UTF-8 -*-
# python3

from devolib import DynamicObject
from devolib.util_log import LOG_D, LOG_E
from devolib.util_os import get_env_var
from devolib.util_str import ends_with

import random
import string
from decimal import Decimal

import mysql.connector # mysql-connector-python

# MARK: Custom Rule

FIELDS_RULE={
    # stat_project_month_area_free
    'area_shop': DynamicObject(min=1000, max=50000),
    'area_ground': DynamicObject(min=1000, max=50000),
    'area_shop_num': DynamicObject(min=100, max=9999),
    'area_ground_num': DynamicObject(min=100, max=9999),

    # stat_project_month_area_rent
    'rent_rate': DynamicObject(min=1, max=100),
    'rent_rate_y': DynamicObject(min=1, max=10),
    'rent_rate_m': DynamicObject(min=1, max=10),

    # stat_project_month_area_sale_rate unused, skip

    # stat_project_month_rent_avg
    'rent_avg': DynamicObject(min=1, max=100),
    'rent_avg_y': DynamicObject(min=1, max=10),
    'rent_avg_m': DynamicObject(min=1, max=10),

    # stat_project_month_collect_rate
    'collect_rate': DynamicObject(min=1, max=100),
    'collect_rate_y': DynamicObject(min=1, max=10),
    'collect_rate_m': DynamicObject(min=1, max=10),

    # stat_project_month_flow_person
    'flow_person': DynamicObject(min=320030, max=1000000),
    'flow_person_y': DynamicObject(min=1, max=10),
    'flow_person_m': DynamicObject(min=1, max=10),

    # stat_project_month_flow_car
    'flow_car': DynamicObject(min=120030, max=500000),
    'flow_car_y': DynamicObject(min=1, max=10),
    'flow_car_m': DynamicObject(min=1, max=10),

    # stat_project_month_rent
    'open_rate': DynamicObject(min=1, max=100),
    'fopen_rate_y': DynamicObject(min=1, max=10),
    'open_rate_m': DynamicObject(min=1, max=10),
    'area_build': DynamicObject(min=5000, max=100000),
    'area_rent': DynamicObject(min=5000, max=100000),
    'area_free': DynamicObject(min=5000, max=100000),
    'area_renting': DynamicObject(min=5000, max=100000),
    'ground_rent': DynamicObject(min=5000, max=100000),
    'berth_free': DynamicObject(min=2000, max=10000),
    'berth_free_y': DynamicObject(min=1, max=10),
    'berth_free_m': DynamicObject(min=1, max=10),
    'open_rate_num': DynamicObject(min=1, max=100),

    # stat_project_month_sale_summary
    'day_avg_report_rate': DynamicObject(min=1, max=100),
    'day_avg_verify_rate': DynamicObject(min=1, max=100),
    'sale_price_avg': DynamicObject(min=200, max=3000),
    'sale_price_avg_y': DynamicObject(min=1, max=10),
    'sale_price_avg_m': DynamicObject(min=1, max=10),
    'sale_pct': DynamicObject(min=1, max=100),

    # stat_project_month_rent_to_open

    # stat_project_month_rent_and_open

    # stat_project_month_collect
    'rent_collecting': DynamicObject(min=100000, max=10000000),
    'rent_collected': DynamicObject(min=100000, max=10000000),
    'collecte_rate': DynamicObject(min=1, max=100),
    'collecte_rate_num': DynamicObject(min=1, max=100),

    # stat_project_month_collect_rate unused, skip

    # stat_project_month_person_car_flow
    'person_flow': DynamicObject(min=100000, max=1000000),
    'car_flow': DynamicObject(min=100000, max=1000000),
    'person_flow_num': DynamicObject(min=100000, max=1000000),
    'car_flow_num': DynamicObject(min=100000, max=1000000),

    # stat_project_month_sale_area_rate
    'sale_amount': DynamicObject(min=10000000, max=100000000),
    'area_rate': DynamicObject(min=1, max=100),
    'sale_amount_num': DynamicObject(min=10000000, max=100000000),
    'area_rate_num': DynamicObject(min=1, max=100),

    # stat_project_month_cate_sale_area

    # stat_project_month_points_consume
    'points': DynamicObject(min=10000000, max=100000000),
    'points_y': DynamicObject(min=1, max=10),
    'points_m': DynamicObject(min=1, max=10),
    'points_rate': DynamicObject(min=1, max=100),
    'points_rate_num': DynamicObject(min=1, max=100),

    # stat_project_month_points_consume, stat_project_month_pay_prefer
    'rate': DynamicObject(min=1, max=100),
    'rate_y': DynamicObject(min=1, max=10),
    'rate_m': DynamicObject(min=1, max=10),
    'rate_num': DynamicObject(min=1, max=100),

}

MONTH_RULE={}

# MARK: Generator

def generate_name():
    first_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_rate(min_value=1, max_value=1000):
    return f"{random.randint(min_value, max_value)}%"

def generate_integer(min_value=1, max_value=1000):
    return random.randint(min_value, max_value)

def generate_decimal(min_value=1.0, max_value=1000.0):
    # 生成一个在[min_value, max_value]范围内的随机Decimal数，保留两位小数
    random_value = random.uniform(min_value, max_value)
    return Decimal(f"{random_value:.2f}")

# MARK: Sql operator

def mock_by_update(connection_info, table_name):
    conn = mysql.connector.connect(**connection_info)
    cursor = conn.cursor()

    # 获取表的字段信息
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    column_names = [column[0] for column in columns]

    # 扫描记录并更新
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()

    for record in records:
        update_data = DynamicObject()

        for i, column in enumerate(columns):
            column_name = column[0]
            column_type = column[1]

            if column_name in FIELDS_RULE:
                rule = FIELDS_RULE[column_name]

                # 2024-10-17 15:52:38,784 DEBUG [mock_mysql.py:43] column_name: id, column_type: int unsigned
                # 2024-10-17 15:52:38,784 DEBUG [mock_mysql.py:43] column_name: date, column_type: varchar(32)
                # 2024-10-17 15:52:38,784 DEBUG [mock_mysql.py:43] column_name: project_id, column_type: int
                # 2024-10-17 15:52:38,785 DEBUG [mock_mysql.py:43] column_name: floor, column_type: varchar(32)
                # 2024-10-17 15:52:38,785 DEBUG [mock_mysql.py:43] column_name: area_shop, column_type: varchar(32)
                # 2024-10-17 15:52:38,786 DEBUG [mock_mysql.py:43] column_name: area_ground, column_type: varchar(32)
                # 2024-10-17 15:52:38,786 DEBUG [mock_mysql.py:43] column_name: area_shop_num, column_type: decimal(6,2)
                # 2024-10-17 15:52:38,786 DEBUG [mock_mysql.py:43] column_name: area_ground_num, column_type: decimal(6,2)
                # LOG_D(f'column_name: {column_name}, column_type: {column_type}')

                ############################## 特殊字段，优先处理
                if ends_with(column_name.lower(), ('_y', '_m')):
                    if 'int' in column_type:
                        update_data.__setattr__(column_name, generate_integer(rule.min, rule.max)) 
                    elif 'varchar' in column_type or 'char' in column_type:
                        update_data.__setattr__(column_name, generate_rate(rule.min, rule.max))

                elif ends_with(column_name.lower(), 'rate'):
                    if 'int' in column_type:
                        update_data.__setattr__(column_name, generate_integer(rule.min, rule.max))  # 自定义范围
                    elif 'varchar' in column_type or 'char' in column_type:
                        update_data.__setattr__(column_name, generate_rate(rule.min, rule.max))  # 自定义范围

                ############################## 整型
                elif 'int' in column_type:
                    update_data.__setattr__(column_name, generate_integer(rule.min, rule.max))  # 自定义范围

                ############################## 字符串
                elif 'varchar' in column_type or 'char' in column_type:
                    if 'name' in column_name.lower():
                        update_data.__setattr__(column_name, generate_name())
                    else:
                        # update_data.__setattr__(column_name, ''.join(random.choices(string.ascii_letters + string.digits, k=10)))

                        # 特殊逻辑，生成数值，填入字符串
                        update_data.__setattr__(column_name, f'{generate_integer(rule.min, rule.max)}')

                ############################## 浮点数
                elif 'decimal' in column_type or 'float' in column_type:
                    update_data.__setattr__(column_name, generate_decimal(rule.min, rule.max))  # 自定义范围

        # 构建 SQL 更新语句
        set_clause = ', '.join(f"{key} = %s" for key in vars(update_data).keys())
        sql = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"  # 假设有一个 id 字段作为主键

        LOG_D(f'sql: {sql}')

        # 执行更新操作
        cursor.execute(sql, (*vars(update_data).values(), record[0]))  # 假设第一个字段是 id
        conn.commit()

            # # 根据类型生成不同的数据
            # if 'int' in column_type:
            #     update_data.__setattr__(column_name, generate_integer())

            # elif 'varchar' in column_type or 'char' in column_type:
            #     if 'name' in column_name.lower():
            #         update_data.__setattr__(column_name, generate_name())
            #     else:
            #         update_data.__setattr__(column_name, ''.join(random.choices(string.ascii_letters + string.digits, k=10)))

            # elif 'rate' in column_name.lower():
            #     update_data.__setattr__(column_name, generate_rate())

            # elif 'decimal' in column_type or 'float' in column_type:
            #     update_data.__setattr__(column_name, generate_decimal())

    # 关闭连接
    cursor.close()
    conn.close()

def mock_by_create(connection_info, table_name):
    pass

# MARK: Command
def cmd_handle(args):
    connection_info = {
        'user': get_env_var('MOCK_MYSQL_USER'),
        'password': get_env_var('MOCK_MYSQL_PASS'),
        'host': get_env_var('MOCK_MYSQL_HOST'),
        'database': get_env_var('MOCK_MYSQL_SCHEMA'),
    }

    table_name = args.table

    mock_by_update(connection_info, table_name)

def cmd_regist(subparsers):
    parser = subparsers.add_parser('mock.mysql', help='mock data for mysql.')
    parser.add_argument('-t', '--table', type=str, default=None, help='table name')
    parser.set_defaults(handle=cmd_handle)


if __name__ == '__main__':
    # sale
    # args = DynamicObject(table='stat_project_month_area_rent')
    # args = DynamicObject(table='stat_project_month_rent_avg')
    # args = DynamicObject(table='stat_project_month_collect_rate')
    # args = DynamicObject(table='stat_project_month_flow_person')
    # args = DynamicObject(table='stat_project_month_flow_car')
    # args = DynamicObject(table='stat_project_month_rent')
    # args = DynamicObject(table='stat_project_month_member_summary')
    # args = DynamicObject(table='stat_project_month_sale_summary')
    # args = DynamicObject(table='stat_project_month_area_free')
    # args = DynamicObject(table='stat_project_month_rent_to_open')
    # args = DynamicObject(table='stat_project_month_rent_and_open')
    # args = DynamicObject(table='stat_project_month_collect')
    # args = DynamicObject(table='stat_project_month_person_car_flow')
    # args = DynamicObject(table='stat_project_month_sale_area_rate')
    args = DynamicObject(table='stat_project_month_cate_sale_area')
    
    # stat_project_month_sale_warn
    # stat_project_month_debts_tenant
    
    # member
    args = DynamicObject(table='stat_project_month_points_consume')
    args = DynamicObject(table='stat_project_month_pay_prefer')
    
    
    
    cmd_handle(args)