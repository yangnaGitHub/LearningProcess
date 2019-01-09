with open("024_FileIoFile.txt", "wt") as out_file:
    out_file.write("024_FileIoFile.txt")

with open("024_FileIoFile.txt", "rt") as in_file:
    text = in_file.read()

print(text)
