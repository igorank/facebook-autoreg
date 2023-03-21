import os
import psutil
import subprocess


class AdbManager:

    all_indices = []
    runned_devices = []
    devices_dict = {}

    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(AdbManager, cls).__new__(cls)
    #     return cls.instance

    # def __init__(self):
    #     super().__init__()
        # self.runned_devices = []
        # self.devices_dict = {}

    @staticmethod
    def is_running():
        '''
        Check if appium server (Node) is already running.
        '''
        # Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if 'adb'.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    @staticmethod
    def get_connected_devices():
        # sub_process = subprocess.Popen("adb devices", shell=True,
        #                                stdout=subprocess.PIPE)
        if not AdbManager.is_running():
            print("Adb is not running. Starting adb...")
            # subprocess.Popen("C:\\Users\\Igor\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe start-server",
            #                  shell=True) # org
            subprocess.call("adb.exe start-server", shell=False)
            # time.sleep(20) # delay for adb init (TEMP?)

        # sub_process = subprocess.Popen("C:\\Users\\Igor\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe devices", shell=True,
        #                                stdout=subprocess.PIPE) # org
        sub_process = subprocess.Popen("adb.exe devices", shell=True, stdout=subprocess.PIPE)
        sub_process_return = str(sub_process.stdout.read())
        res = [i for i in range(len(sub_process_return)) if sub_process_return.startswith("tdevice", i)]
        lst = []
        for i in res:
            if sub_process_return[i - 15] == 'n':
                lst.append(sub_process_return[i - 14:i - 1])
            else:
                lst.append(sub_process_return[i - 15:i - 1])
        return lst

    @staticmethod
    def add_launched_device(device_name):
        AdbManager.runned_devices.append(str(device_name))

    @staticmethod
    def remove_launched_device(device_name):
        AdbManager.runned_devices.remove(str(device_name))

    @staticmethod
    def get_list_of_launched_devices():
        return AdbManager.runned_devices

    @staticmethod
    def get_list_difference(list1, list2):
        dif = [item for item in list1 if item not in list2]
        return dif

    @staticmethod
    def add_index_to_dic(index, device_name):
        AdbManager.devices_dict[index] = str(device_name)
        AdbManager.all_indices.append(str(index))

    @staticmethod
    def get_dict():
        return AdbManager.devices_dict

    @staticmethod
    def get_dict_value_by_key(key):
        return AdbManager.devices_dict[key]

    @staticmethod
    def delete_index_from_dict(index):
        del AdbManager.devices_dict[index]

    @staticmethod
    def execute_command(device_name, command):
        devnull = open(os.devnull, 'wb')
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # print("C:\\Users\\Igor\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe -s " + str(device_name) + " " + str(command)) # DEBUG
        # subprocess.Popen("C:\\Users\\Igor\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe -s " + str(device_name) + " " + str(command), shell=True) # org
        subprocess.call("adb.exe -s " + str(device_name) + " " + str(command), shell=False, stdout=devnull, stderr=devnull, startupinfo=startupinfo)
        #subprocess.Popen("adb -s " + str(device_name) + " " + str(command), shell=True)
        # sub_process_return = str(sub_process.stdout.read())
        # index = sub_process_return.find(str("Success"))
        # res = sub_process_return[index:index + 7]
        # if res == "Success":
        #     return True
        # else:
        #     return False