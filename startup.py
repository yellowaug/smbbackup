from backupsmb import BackupSMB
import sys





# 配置你的SMB备份设置
def callbakup_action(folder):
    smb_backup = BackupSMB(folder) #传入要备份的共享文件夹的名称
    # smb_backup.backup(r"D:\testbak")
    smb_server_path = f"\\\\{smb_backup.backup_host}\\\\{smb_backup.backup_floder_name}"  # 检索的目录
    # time_tamp=smb_backup.getRemoteFileStatFinalChangeTime(smb_server_path)
    smb_backup.copy_files(smb_server_path) #备份文件

    smb_backup.close_session() #关闭连接
if __name__=='__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-fn' and len(sys.argv[2:])>0:
            for arg in sys.argv[2:]: #从参数-fn后面开始
                print(f"获取到的文件夹列表是：{arg}")
                callbakup_action(arg)
        else:
            print("参数错误,请使用-fn参数 \n"
                  "示例: python backup_smb.py -fn 文件夹1 文件夹2 文件夹3")
    # callbakup_action()