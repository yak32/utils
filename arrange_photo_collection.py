
#if __name__=='__main__':
#    try:
#        jpeg_dir = 'D:\\photos\\output'
#        cr2_dir = 'E:\\photos\\temp'

#        cr2_names = set()
#        cr2_names = os.listdir(cr2_dir)

#        jpg_names = set()
#        jpg_names = os.listdir(jpeg_dir)

#        for cr2 in cr2_names:
#            file_jpeg = os.path.splitext(cr2)[0] + '.JPG'
#            if file_jpeg in jpg_names:
#                os.remove(os.path.join(cr2_dir,cr2))

#        print 'success'
#    except Error:
#        print 'exception'


from PIL import Image

import os
import re
import sys
import time
import shutil

CREATE_HARDLINK=0

def extract_jpeg_exif_time(jpegfn):
    if not os.path.isfile(jpegfn):
        return None
    try:
        im = Image.open(jpegfn)
        if hasattr(im, '_getexif'):
            exifdata = im._getexif()
            ctime = exifdata[0x9003]
            #print ctime
            return ctime
    except:
        _type, value, traceback = sys.exc_info()
        print "Error:\n%r", value

    return None

def get_exif_prefix(jpegfn):
    ctime = extract_jpeg_exif_time(jpegfn)
    if ctime is None:
        return None
    ctime = ctime.replace(':', '/')
    ctime = re.sub('[^\d]+', '_', ctime)
    return ctime

def move_jpeg_file(fn):
    if not os.path.isfile(fn):
        return 0
    ext = os.path.splitext(fn)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.jfif']:
        return 0
    path, base = os.path.split(fn)
    print base # status
    prefix = get_exif_prefix(fn)
    if prefix is None:
        return 0
    if base.startswith(prefix):
        return 0 # file already renamed to this prefix

    month = ''
    month += prefix[5];
    month += prefix[6];

    day = ''
    day += prefix[8];
    day += prefix[9];

    new_path = os.path.join(path, '..');
    new_path = os.path.join(new_path, 'sorted');
    new_path = os.path.join(new_path, month);
    new_path = os.path.join(new_path, day);
    
    if not os.path.isdir(new_path):
        os.makedirs( new_path, 0755 );

    new_path = os.path.join(new_path, base);
    shutil.move(fn, new_path)

    return 1

def move_jpeg_files_in_dir(dn):
    names = os.listdir(dn)
    count=0
    for n in names:
        file_path = os.path.join(dn, n)
        if os.path.isfile(file_path):
            count += move_jpeg_file(file_path)
    return count


if __name__=='__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        print '''Usage:  

  process.py  dir   
  supports [jpeg|jpg|jfif]

'''
    move_jpeg_files_in_dir(path)
