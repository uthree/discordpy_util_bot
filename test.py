from mylibrary.filesystem import *

fs = FileSystem()

dir1 = Directory("dir1", fs, fs)
fs.append(dir1)

dir2 = Directory("dir2", dir1, fs)
dir1.append(dir2)

dir3 = Directory("dir3", dir2, fs)
dir2.append(dir3)

text = TextFile("file1", dir2, fs)
dir2.append(text)

print(fs.get_content_from_absolute_path("/dir1/dir2/dir3").name)