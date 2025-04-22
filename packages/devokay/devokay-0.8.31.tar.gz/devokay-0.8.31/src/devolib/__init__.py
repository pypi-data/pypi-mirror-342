# -*- coding: UTF-8 -*-
# python3


'''
    # 创建动态对象
    obj = DynamicObject(name="Alice", age=30, rate="10%")
    
    # 访问动态属性
    print(obj.name)  # 输出: Alice
    print(obj.age)   # 输出: 30
    print(obj.rate)  # 输出: 10%

    # 动态添加新属性
    obj.address = "123 Main St"
    print(obj.address)  # 输出: 123 Main St
'''
class DynamicObject:
    def __init__(self, **kwargs):
        # 动态设置属性
        for key, value in kwargs.items():
            # if isinstance(value, dict):  # 如果属性值是字典（可能是另一个DynamicObject）
            #     value = DynamicObject(**value)
            setattr(self, key, value)

    def __repr__(self):
        return f"<DynamicObject {vars(self)}>"