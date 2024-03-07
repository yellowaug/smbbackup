import logging
import os
from smbclient import listdir, register_session, delete_session,stat,open_file
from smbclient.path import isdir
from smbclient.shutil import copyfileobj
from datetime import datetime
from dotenv import load_dotenv

class BackupSMB:

    def __init__(self, floder_name:str)\
            ->None:
        """
        初始化SMB备份类
        :param floder_name: 共享中文件夹
        :return: None
        """
        load_dotenv() #不使用该方法无法获取.env文件中的变量值
        self.backup_floder_name = floder_name
        self.backup_host = os.getenv("SMB_SERVER")
        self.backup_user = os.getenv("SMB_USER")
        self.backup_password = os.getenv("SMB_PASSWORD")
        self.local_floder_path = os.getenv("LOCAL_BAK_DIR")
        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        register_session(self.backup_host,self.backup_user,self.backup_password) #连接到SMB服务器

    def getRemoteFileStatFinalChangeTime(self,remote_file_path):
        """
        获取远程文件的最后修改时间
        :param remote_file_path: 远程文件路径
        :return: 返回最后修改时间的时间戳
        """
        timestamp=stat(remote_file_path).st_mtime_ns
        # self.log.info(f"获取到远程文件的最后修改时间{timestamp}")
        return timestamp

    def checkFileChangeTime(self,file_timestamp):
        """
        检查文件最后修改时间是否大于备份时间
        :param file_timestamp: 文件最后修改时间的时间戳，这里直接传入时间戳即可
        :return: True or False
        """
        # 获取比较备份文件的时间标签
        bak_start_timestamp = datetime.strptime(os.environ.get("BAK_TIMESTAMP"), "%Y-%m-%d %H:%M:%S")
        self.log.info(f"标定的备份标签：{bak_start_timestamp}")
        # 获取文件的最后修改时间
        readable_date = datetime.fromtimestamp(file_timestamp / 1e9).strftime('%Y-%m-%d %H:%M:%S')
        file_finenal_change_time = datetime.strptime(readable_date, "%Y-%m-%d %H:%M:%S")
        self.log.info(f"文件最后修改时间:{file_finenal_change_time}")
        if file_finenal_change_time > bak_start_timestamp:
            return True
        else:
            return False
    def checkFileName(self,remote_path:str):
        """
        检查文件是否是
        :param remote_path:
        :return:
        """
        return remote_path.startswith(".")


    def copy_files(self,remote_path:str)->None:
        """
        文件复制函数，把远程目录下的文件以及文件夹复制到本地目录下，该函数有递归方法
        :param remote_path: SMB上的远程文件路径
        :return:
        """

        try:
            for entry in listdir(remote_path):
                remote_entry_path = os.path.join(remote_path, entry)
                local_entry_path = os.path.join(self.local_floder_path, entry)
                print(entry)
                #获取文件时间，判断文件或者文件夹是否满足备份的时间要求。
                check_time_tag=self.getRemoteFileStatFinalChangeTime(remote_entry_path)
                isbak=self.checkFileChangeTime(check_time_tag)
                if isbak and not self.checkFileName(remote_entry_path): #检测备份时间，以及是否是系统文件
                    if isdir(remote_entry_path) :
                        if not os.path.exists(local_entry_path):
                            os.makedirs(local_entry_path)
                        #还要判断文件是否存在，比对本地文件和远程文件的时间戳，如果需要本地文件已经存在，
                        #且是已经备份过的文件，则不需要复制，否则需要进行复制备份
                        self.copy_files(remote_entry_path)
                    else:
                        if not os.path.exists(os.path.dirname(local_entry_path)):
                            os.makedirs(os.path.dirname(local_entry_path))
                        with open_file(remote_entry_path, mode='rb') as remote_file:
                            with open(local_entry_path, 'wb') as local_file:
                                copyfileobj(remote_file, local_file)
                else:
                    print(f"{remote_entry_path} 不需要备份")
        except Exception as e:
            print(f"Error copying {remote_path} to {self.local_floder_path}: {e}")
    # def backup(self,local_back_floatpath)->None:
    #     """
    #     备份文件夹，备份逻辑是，根据最后修改时间是否大于标定时间，大于的则备份，小于的不备份
    #     使用最后修改时间的好处是，不管文件是新建或者修改，只要大于标定时间都进行备份.
    #     备份完成后关闭连接
    #     :param local_back_floatpath: 备份到本地文件夹的路径
    #     :return: None
    #     """
    #     smb_server_path = f"\\\\{self.backup_host}\\\\{self.backup_path}" #检索的目录
    #     self.log.info(f"开始备份文件夹{smb_server_path}")
    #     for file in listdir(smb_server_path):
    #         #判断不是文件名称不是”.*"类型的文件
    #         if file.startswith(".")  :
    #             self.log.info(f"跳过文件夹{file}，该文件是系统文件")
    #             pass
    #         else:
    #             will_be_back_file_path=os.path.join(smb_server_path,file)
    #             file_info=stat(will_be_back_file_path)
    #             # 获取比较备份文件的时间标签
    #             bak_start_timestamp=datetime.strptime(os.environ.get("BAK_TIMESTAMP"),"%Y-%m-%d %H:%M:%S")
    #             #获取文件的最后修改时间
    #             file_timestamp = file_info.st_mtime_ns
    #             readable_date = datetime.fromtimestamp(file_timestamp / 1e9).strftime('%Y-%m-%d %H:%M:%S')
    #             file_finenal_change_time = datetime.strptime(readable_date, "%Y-%m-%d %H:%M:%S")
    #             if file_finenal_change_time>bak_start_timestamp: #时间比较
    #                 if isdir(will_be_back_file_path):
    #                     self.log.info(f"检测到该目录是文件夹{smb_server_path}，开始备份文件夹")
    #                     # smb_server_path = will_be_back_file_path
    #                     # self.backup(local_back_floatpath) #递归查询
    #                     bak_dst=os.path.join(local_back_floatpath,file)
    #                     # copytree(src=will_be_back_file_path, dst=bak_dst)
    #                 else:
    #                     self.log.info(f"开始备份文件{will_be_back_file_path}")
    #                     copy(src=will_be_back_file_path,dst=local_back_floatpath)
    #             else:
    #                 self.log.info(f"文件{will_be_back_file_path}无需备份")

    def close_session(self):
        # 关闭连接会话
        delete_session(self.backup_host)
