import os
import time
import subprocess
import random
import string
from randommodelgen import RandomModelGenerator
from randcoordgenerator import RandCoordGenerator
from filemanager import FileManager

devnull = open(os.devnull, 'wb')


class Ldconsole:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    spath_to_ldplayer = None

    def __init__(self):
        super().__init__()
        self.path_to_ldplayer = None
        self.fingerprints = FileManager.get_filesdata("useragents//android_finger.txt")

    def set_path(self, path_to_ldplayer):
        self.path_to_ldplayer = path_to_ldplayer
        Ldconsole.spath_to_ldplayer = path_to_ldplayer

    def get_path(self):
        return self.path_to_ldplayer

    @staticmethod
    def get_spath():
        return Ldconsole.spath_to_ldplayer

    def launch(self, mnq_name):
        subprocess.call(self.path_to_ldplayer + "ldconsole.exe launch --name "
                        + str(mnq_name), shell=False, stdout=devnull,
                        stderr=devnull, startupinfo=Ldconsole.startupinfo)
        print("Profile " + str(mnq_name) + " has been launched")

    def quit(self, mnq_name):
        subprocess.call(self.path_to_ldplayer + "ldconsole.exe quit --name "
                        + str(mnq_name), shell=False, stdout=devnull,
                        stderr=devnull, startupinfo=Ldconsole.startupinfo)
        print("Profile " + str(mnq_name) + " has been stopped")
        time.sleep(5)

    def add(self, mnq_name):
        subprocess.call(self.path_to_ldplayer + "ldconsole.exe add --name "
                        + str(mnq_name), shell=False, stdout=devnull,
                        stderr=devnull, startupinfo=Ldconsole.startupinfo)
        # time.sleep(4)
        print("Profile " + str(mnq_name) + " has been added")

    def remove(self, mnq_name):
        subprocess.call(self.path_to_ldplayer + "ldconsole.exe remove --name "
                        + str(mnq_name), shell=False, stdout=devnull,
                        stderr=devnull, startupinfo=Ldconsole.startupinfo)
        print("Profile " + str(mnq_name) + " has been deleted")

    def remove_by_index(self, mnq_idx):
        subprocess.call(self.path_to_ldplayer + "ldconsole.exe remove --index "
                        + mnq_idx, shell=False, stdout=devnull, stderr=devnull,
                        startupinfo=Ldconsole.startupinfo)

    def install_app(self, mnq_name, app_name):
        subprocess.call(self.path_to_ldplayer + "ldconsole.exe installapp --name "
                        + str(mnq_name) + " --filename " + str(app_name), shell=False,
                        stdout=devnull, stderr=devnull, startupinfo=Ldconsole.startupinfo)

    def modify(self, mnq_name, p_number):
        manufacturer = RandomModelGenerator.get_manufacturer()
        subprocess.call(
            self.path_to_ldplayer + "ldconsole.exe modify --name " + str(mnq_name) +
            " --cpu 2 --memory 1536 --pnumber " + str(p_number)
            + " --resolution 540,960,240" +
            " --manufacturer " + manufacturer + " --model "
            + "\"" + RandomModelGenerator.get_mob_model(
                manufacturer) + "\"",
            shell=False, stdout=devnull, stderr=devnull, startupinfo=Ldconsole.startupinfo)
        print("Profile " + str(mnq_name) + " has been changed")

    def execute_adb_command_by_index(self, mnq_idx, command):
        subprocess.Popen(self.path_to_ldplayer + "ldconsole.exe adb --index " + str(mnq_idx)
                         + " --command " + "\"" + str(command) + "\"",
                         shell=False, startupinfo=Ldconsole.startupinfo)
        print(str(self.path_to_ldplayer + "ldconsole.exe adb --index " + str(
            mnq_idx) + " --command " + "\"" + command + "\""))

    @staticmethod
    def serial_generator():
        serial = '00' + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        return serial

    def randomize_settings(self, mnq_idx, geo, randomize_f_s=False):
        randcordinator = RandCoordGenerator()
        n_cord, e_cord = randcordinator.get_rand_coord(geo)
        # manufacturer = RandomModelGenerator.get_manufacturer()
        # mob_model = RandomModelGenerator.get_mob_model(manufacturer)

        fingerprint = random.choice(self.fingerprints)

        # startupinfo = subprocess.STARTUPINFO()
        # startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.call(self.path_to_ldplayer + "ldconsole.exe setprop --index " + str(
            mnq_idx) + " --key " + "\"" + "phone.imei" + "\""
                        + " --value " + "\"" + "auto" + "\"", shell=False,
                        stdout=devnull, stderr=devnull,
                        startupinfo=Ldconsole.startupinfo)
        subprocess.call(self.path_to_ldplayer + "ldconsole.exe setprop --index " + str(
            mnq_idx) + " --key " + "\"" + "phone.imsi" + "\""
                        + " --value " + "\"" + "auto" + "\"", shell=False,
                        stdout=devnull, stderr=devnull, startupinfo=Ldconsole.startupinfo)
        subprocess.call(self.path_to_ldplayer + "ldconsole.exe setprop --index " + str(
            mnq_idx) + " --key " + "\"" + "phone.simserial" + "\""
                        + " --value " + "\"" + "auto" + "\"", shell=False,
                        stdout=devnull, stderr=devnull, startupinfo=Ldconsole.startupinfo)
        subprocess.call(self.path_to_ldplayer + "ldconsole.exe setprop --index " + str(
            mnq_idx) + " --key " + "\"" + "phone.androidid" + "\""
                        + " --value " + "\"" + "auto" + "\"", shell=False,
                        stdout=devnull, stderr=devnull, startupinfo=Ldconsole.startupinfo)
        subprocess.call(self.path_to_ldplayer + "ldconsole.exe locate --index " + str(
            mnq_idx) + " --LLI " + str(e_cord) + "," + str(n_cord),
                        shell=False, stdout=devnull, stderr=devnull,
                        startupinfo=Ldconsole.startupinfo)
        if randomize_f_s:
            subprocess.call(self.path_to_ldplayer + "ldconsole.exe setprop --index " + str(
                mnq_idx) + " --key " + "\"" + "ro.serialno" + "\"" + " --value " + "\"" + str(
                self.serial_generator()) + "\"", shell=False, stdout=devnull, stderr=devnull,
                            startupinfo=Ldconsole.startupinfo)
            subprocess.call(self.path_to_ldplayer + "ldconsole.exe setprop --index " + str(
                mnq_idx) + " --key " + "\"" + "ro.build.fingerprint" + "\"" + " --value " + "\"" + str(
                fingerprint) + "\"", shell=False, stdout=devnull, stderr=devnull,
                            startupinfo=Ldconsole.startupinfo)

    def get_fingerprint(self, mnq_idx):
        sub_process = subprocess.Popen(self.path_to_ldplayer + "ldconsole.exe getprop --index " + str(
            mnq_idx) + " --key " + "\"" + "ro.build.fingerprint" + "\"", shell=True, stdout=subprocess.PIPE)
        sub_process_return = sub_process.stdout.read()
        return sub_process_return.decode('utf-8')

    def get_serialno(self, mnq_idx):
        sub_process = subprocess.Popen(self.path_to_ldplayer + "ldconsole.exe getprop --index " + str(
            mnq_idx) + " --key " + "\"" + "ro.serialno" + "\"", shell=True, stdout=subprocess.PIPE)
        sub_process_return = sub_process.stdout.read()
        return sub_process_return.decode('utf-8')

    # def get_imei(self, mnq_idx):
    #     sub_process = subprocess.Popen(self.path_to_ldplayer + "ldconsole.exe getprop --index " + str(
    #         mnq_idx) + " --key " + "\"" + "phone.imei" + "\"", shell=True, stdout=subprocess.PIPE)
    #     sub_process_return = sub_process.stdout.read()
    #     return sub_process_return.decode('utf-8')

    # def get_imsi(self, mnq_idx):
    #     sub_process = subprocess.Popen(self.path_to_ldplayer + "ldconsole.exe getprop --index " + str(
    #         mnq_idx) + " --key " + "\"" + "phone.imsi" + "\"", shell=True, stdout=subprocess.PIPE)
    #     sub_process_return = sub_process.stdout.read()
    #     return sub_process_return.decode('utf-8')

    # def get_androidid(self, mnq_idx):
    #     sub_process = subprocess.Popen(self.path_to_ldplayer + "ldconsole.exe getprop --index " + str(
    #         mnq_idx) + " --key " + "\"" + "phone.androidid" + "\"", shell=True, stdout=subprocess.PIPE)
    #     sub_process_return = sub_process.stdout.read()
    #     return sub_process_return.decode('utf-8')

    def get_profile_index(self, mnq_name):
        sub_process = subprocess.Popen(self.path_to_ldplayer + "ldconsole.exe list2", shell=False,
                                       stdout=subprocess.PIPE, startupinfo=Ldconsole.startupinfo)
        sub_process_return = str(sub_process.stdout.read())
        index = sub_process_return.find(str(mnq_name))
        character = sub_process_return[index - 3]
        if character.isdigit():
            return str(sub_process_return[index - 3] + sub_process_return[index - 2])
        return sub_process_return[index - 2]

    # def get_list_of_profiles(self):
    #     listoffiles = os.listdir(self.path_to_ldplayer + r'\vms\config')
    #     listoffiles.remove('leidians.config')
    #     listoffiles.remove('leidian0.config')
    #     listoffiles.remove('firstboottag')
    #     return listoffiles

    def find_num_of_line(self, mnq_idx):
        lookup = '"basicSettings.fsAutoSize": 1'
        with open(self.path_to_ldplayer + r'\vms\config\leidian'
                  + str(mnq_idx) + '.config') as my_file:
            for num, line in enumerate(my_file, 1):
                if lookup in line:
                    return num

    def set_location(self, mnq_idx, line, cord_n, cord_e):
        with open(self.path_to_ldplayer + r'\vms\config\leidian'
                  + str(mnq_idx) + '.config', 'r') as file:
            data = file.readlines()
        data[line + 1] = '    "statusSettings.location": {\n'
        with open(self.path_to_ldplayer + r'vms\config\leidian'
                  + str(mnq_idx) + '.config', 'w') as file:
            file.writelines(data)
            file.write('        "lng": ' + cord_e + ',\n')
            file.write('        "lat": ' + cord_n + '\n')
            file.write('    }\n')
            file.write('}')

    def set_debug_mode(self, mnq_idx, line):
        with open(self.path_to_ldplayer + r'\vms\config\leidian'
                  + str(mnq_idx) + '.config', 'r') as file:
            data = file.readlines()
        data[line - 1] = '    "basicSettings.fsAutoSize": 1,\n'
        data[line] = '    "basicSettings.adbDebug": 1,\n'
        with open(self.path_to_ldplayer + r'\vms\config\leidian'
                  + str(mnq_idx) + '.config', 'w') as file:
            file.writelines(data)
            file.write('}')
