from moto.platform.macos.component.file import File  # type: ignore



#file_object = File(path = "tests/env/sample.txt")
ex_path = "/Users/xingxing/Desktop/CCL其他话题词汇.pages"
file_object = File(path = ex_path)
print(file_object.__dict__())

print(str(file_object))


nex_path = "/Users/xingxing/Desktop/CCL其他话题词汇 2.pages"
file_object = File(path = nex_path)
print(file_object.__dict__())

print(str(file_object))