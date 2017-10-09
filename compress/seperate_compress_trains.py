import os
import zipfile

trainsdir = "/Users/jaeyoung/workspace/PycharmProjects/fast-style-transfer/data/train2014/"
zipdir = "/Users/jaeyoung/workspace/PycharmProjects/fast-style-transfer/data/train2014/zip"

zipfileio = list()
num_zipfile = [0,] * 30
print(num_zipfile)
for target in range(30):
    zipfilename = "train_%02d0k-%02d0k.zip" % (target*2, (target+1)*2)
    print(zipfilename)
    zippath = os.path.join(zipdir, zipfilename)
    zipfileio.append(zipfile.ZipFile(zippath, 'w'))

# zipfileio.write('zip.py', compress_type=zipfile.ZIP_DEFLATED)



i = 0


def numbering(filename):
    numstr = os.path.splitext(filename)[0][-6:]
    numint = int(numstr)
    numint = int(numint/10000)
    label = int(numint / 2)
    return label




def compress_with_label(label, filepath):
    zipfileio[label].write(filepath, os.path.basename(filepath), compress_type=zipfile.ZIP_DEFLATED)
    num_zipfile[label] += 1


for (path, dir, files) in os.walk(trainsdir):
    for filename in files:
        if filename == '.DS_Store':
            continue
        if os.path.splitext(filename)[1] == '.zip':
            continue

        label = numbering(filename)
        # if label == target:
        if not dir == []:
            print("dir %s" % dir)
        filepath = os.path.join(path, filename)
        compress_with_label(label, filepath)
        i += 1
        if i > 500:
            print("%s/%s" % (path, filename))
            print(num_zipfile)
            i = 0

print(num_zipfile)
for each in zipfileio:
    each.close()