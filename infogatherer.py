import os
import sys
from datetime import datetime
import magic
from collections import defaultdict

class Infogatherer:
    def __init__(self,path,options=None):
        if not os.path.isdir(path):
            raise Exception  # TODO: Path does not exist
        else:
            self.path = os.path.abspath(path)
        if options == None:
            self.options = {
                'size':1
            }
        else:
            if not isinstance(options,dict):
                raise Exception #TODO: excludes is not a list
            else:
                self.options = options

        self.invoke_time = datetime.now()

    def _get_directory_size(self,abspath):
        size = 0
        f_count = 0
        for dp,dn,fn in os.walk(abspath):
            for file in fn:
                size += os.path.getsize(dp+'/'+file)/self.options['size']
                f_count += 1
            for dirn in dn:
                s,f = self._get_directory_size(dp+'/'+dirn)
                size += s
                f_count += f
        return size,f_count
    def gather(self):
        start_time = datetime.now()
        l = os.walk(self.path)
        file_list = []
        folder_list = []
        f_extension_list = defaultdict(list,{})
        f_extension_size_list = defaultdict(lambda: 0, {})
        f_type_list = defaultdict(list,{})
        f_type_size_list = defaultdict(lambda :0,{})
        folder_count = 0
        file_count = 0
        for dirpath, dirnames, filenames in l:
            if len(filenames) == 0:
                continue
            folder_count += len(dirnames)
            file_count += len(filenames)
            # folder_list.extend(
            #     [(dirpath + '/' + n, os.path.getsize(dirpath + '/' + n)) for n in dirnames]
            # )
            for n in dirnames:
                folder_list.append((dirpath+'/'+n,self._get_directory_size(dirpath+'/'+n)))
            for name in filenames:
                file_list.append((dirpath + '/' + name, os.path.getsize(dirpath+'/'+name)/self.options['size']))
                type = magic.from_file(dirpath + '/' + name)
                f_type_size_list[type] += 1
                f_type_list[type].append((dirpath + '/' + name,os.path.getsize(dirpath + '/' + name)/self.options['size']))
                if name.startswith('.'):
                    f_extension_size_list['Hidden'] += 1
                    f_extension_list['Hidden'].append((dirpath + '/' + name,os.path.getsize(dirpath + '/' + name)/self.options['size']))
                else:
                    extension = name.split('.')
                    if len(extension) < 2:
                        f_extension_size_list['Unknown'] += 1
                        f_extension_list['Unknown'].append((dirpath + '/' + name,os.path.getsize(dirpath + '/' + name)/self.options['size']))
                    else:
                        f_extension_size_list[extension[-1]] += 1
                        f_extension_list[extension[-1]].append((dirpath + '/' + name,os.path.getsize(dirpath + '/' + name)/self.options['size']))
        end_time = datetime.now()
        return Info(self.path,
            file_list,folder_list,f_extension_list,f_extension_size_list,
            f_type_list,f_type_size_list,folder_count,file_count,end_time - start_time,self.invoke_time
        )


class Info:
    def __init__(self,path,file_list,folder_list,f_extension_list,
                 f_extension_size_list,f_type_list,f_type_size_list,
                 folder_count,file_count,time_taken,invoke_time):
        if path.endswith('/'):
            del path[-1]
        self.path = path
        self.file_list = list(map(lambda x:(x[0].replace(path+'/',''),x[1]),file_list))
        self.folder_list = list(map(lambda x:(x[0].replace(path+'/',''),x[1]),folder_list))
        self.f_extension_list = f_extension_list
        self.f_extension_size_list = f_extension_size_list
        self.f_type_list = f_type_list
        self.f_type_size_list = f_type_size_list
        self.folder_count = folder_count
        self.file_count = file_count
        self.time_taken = time_taken
        self.invoke_time = invoke_time

if __name__ == '__main__':
    i = Infogatherer('/home/aniket/Downloads/American.Pie.Presents.The.Naked.Mile -2006-.DVDRip')
    print(i.gather().file_list)