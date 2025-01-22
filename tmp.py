# import os
# folder_stat = os.stat(
#     '/Users/xingxing/Desktop'
# )

# print(type(folder_stat))
# print(folder_stat)

# import pathlib

# folder_stat = pathlib.Path('/Users/xingxing/Desktop').stat()
# print(type(folder_stat))
# print(folder_stat)

# pip install fs


# from moto.particle.base.item import BaseItem
# from moto.particle.base.folder import BaseFolder

# obj = BaseFolder('/Users/xingxing/Desktop/my-files')
# print(obj.__dict__())
# print(obj.list(recursive=True, reg_prefix = '2024-'))

from moto.particle.custom.xmeta import XMeta

obj = XMeta('/Users/xingxing/Desktop/my-project/x17/tests/env')
print(str(obj))
print(obj.__dict__())

obj2 = XMeta('/Users/xingxing/Desktop/my-project/x17/tests/env/sample.txt')
print(str(obj2))
print(obj2.__dict__())


