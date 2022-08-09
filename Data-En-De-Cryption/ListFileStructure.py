# imports
import os
from sm import makeString


# function for listing the tree of a dictionary
# Originally copied from a Stack-Overflow-Answer, edited for own purposes
def list_files(startpath):
    lFolders = []
    lFiles = []
    p = startpath.split(os.sep)[-1]
    p = "encrypted-" + p
    p = makeString(startpath.split(os.sep)[:-1], os.sep) + p
    p2 = startpath.replace("encrypted-", "")
    if os.path.isfile(p):
        lFiles.append(p)
    elif os.path.isfile(p2):
        lFiles.append(p2)
    elif os.path.isfile(startpath):
        lFiles.append(startpath)
    else:
        for root, dirs, files in os.walk(startpath):
            # repFold = root.replace(sub_path, "")
            lFolders.append(root + "/")

            for f in files:
                file = root + "/" + f
                lFiles.append(file)

    return lFolders, lFiles
