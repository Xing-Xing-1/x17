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
import os

cwd = os.getcwd()

obj2 = XMeta(item_path = f"{cwd}/tests/env/")
print(str(obj2))
print(obj2.export())
obj2.write()


#/Users/xingxing/Desktop/my-project/x17/tests/env/test.txt

obj1 = XMeta(item_path = f"{cwd}/tests/env/test.txt")
print(str(obj1))
obj1.comment("This is good comment.")
obj1.update_tagset(key = 'tag1', value = 'value1')
print(obj1.export())
obj1.write()