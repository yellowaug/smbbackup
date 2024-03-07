import logging
import os
from smbclient import listdir, register_session, scandir,delete_session,stat,open_file
from smbclient.path import isdir
from smbclient.shutil import copy,copy2,copytree,copyfileobj
from datetime import datetime




log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

smb_server="10.12.3.65"
smb_user="test"
smb_psaa="jjck@123"
floder_name="test"
# unc_path=r"\\10.12.3.65\\sync"
unc_path=f"\\\\{smb_server}\\\\{floder_name}"
# Optional - register the server with explicit credentials
session=register_session(smb_server, username=smb_user, password=smb_psaa)
print(session)

def scanf_dir(unc_path):
    for dir in listdir(unc_path):
       # print(dir)
       remove_path=os.path.join(unc_path,dir)
       dir_info=stat(remove_path)
       file_timestamp=dir_info.st_mtime_ns
        #获取文件最后更改时间
       readable_date = datetime.fromtimestamp(file_timestamp / 1e9).strftime('%Y-%m-%d %H:%M:%S')
       date_obj_1=datetime.strptime(readable_date, "%Y-%m-%d %H:%M:%S")
       # 定义日期和时间
       date_str = "2024-02-28 00:00:00"
       # 将字符串转换为datetime对象
       date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
       # 将datetime对象转换为毫秒时间戳
       # milliseconds_timestamp = int(date_obj.timestamp() * 1000)
       # match_timestamp=file_timestamp-milliseconds_timestamp
       # print(file_timestamp)
       # print(milliseconds_timestamp)
       if date_obj>date_obj_1:
           # print("文件最后修改时间大于2024-02-28 00:00:00")

           print("文件最后修改时间小于2024-02-28 00:00:00,该时间节点以前的文件已备份，忽略")
           if isdir(remove_path) and not dir.startswith("."):
               bak_dst = os.path.join(remove_path, dir)
               # copytree(src=bak_dst,dst=r"D:\\testbak")
       else:
           print("文件最后修改时间大于2024-02-28 00:00:00")
       print(f"文件名称:{remove_path},文件最后修改时间:{readable_date}")
       # log.info(dir)
       # log.info(stat(os.path.join(unc_path,dir)))

       # #复制文件到本地
       # if dir !=".stfolder":
       #  copy2(src=remove_path,dst=r"D:\\testbak")
def list_files_and_dirs(path):
    try:
        for entry in scandir(path):
            print(entry.path)
            if entry.is_dir():
                list_files_and_dirs(entry.path)
    except Exception as e:
        print(f"Error accessing {path}: {e}")
def copy_files(remote_path, local_path):
    try:
        for entry in listdir(remote_path):
            remote_entry_path = os.path.join(remote_path, entry)
            local_entry_path = os.path.join(local_path, entry)
            print(entry)
            if isdir(remote_entry_path):
                if not os.path.exists(local_entry_path):
                    os.makedirs(local_entry_path)
                copy_files(remote_entry_path, local_entry_path)
            else:
                if not os.path.exists(os.path.dirname(local_entry_path)):
                    os.makedirs(os.path.dirname(local_entry_path))
                with open_file(remote_entry_path, mode='rb') as remote_file:
                    with open(local_entry_path, 'wb') as local_file:
                        copyfileobj(remote_file, local_file)
    except Exception as e:
        print(f"Error copying {remote_path} to {local_path}: {e}")


# list_files_and_dirs("\\10.12.3.65\\test\smbtest")
copy_files(r"\\10.12.3.65\test", r"D:\testbak")
# for dir in scandir(unc_path):
#    log.info(dir)
# scanf_dir(unc_path)
# copytree(src=r"\\10.12.3.65\\test\smbtest",dst=r"D:\\testbak\smbtest")
#删除注册的session会话
delete_session(smb_server)