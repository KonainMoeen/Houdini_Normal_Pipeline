import subprocess
import os, sys, time
import threading 
from paths import get_houdini_path
 
def locate_houdini():    
    import os
    from winreg import ConnectRegistry, OpenKey, CloseKey, EnumKey, EnumValue, QueryValue, HKEY_LOCAL_MACHINE

    install_path = None
    abort = False
    while install_path is None and not abort:
        try:
            registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            key_path = 'SOFTWARE\\Side Effects Software\\'
            key = OpenKey(registry, key_path)
            i = 0
            while install_path is None:
                sub_key = EnumKey(key, i)
                i += 1
                if sub_key == 'Houdini' or sub_key == 'Houdini Engine':
                    sub_key = OpenKey(key, sub_key)
                    install_path = EnumValue(sub_key, 0)[1]
                    print(install_path)
                    if not os.path.exists(install_path):
                        install_path = None
                    CloseKey(sub_key)
            CloseKey(key)
        except:
            pass

    return install_path

def locate_hython_and_hkey():
    houdini_path = get_houdini_path()
    hython_path = houdini_path + 'bin\\hython3.9.exe'
    hkey_path = houdini_path + 'bin\\hkey.exe'
    assert os.path.exists(hython_path), 'hython not found!'
    assert os.path.exists(hkey_path), 'hython not found!'
    return hython_path, hkey_path

def run_pipeline():
    hython_path, hkey_path = locate_hython_and_hkey()
    subprocess.Popen([hkey_path])
    subprocess.call([hython_path, "New_main.py"])
    
# def bootstrap(argv):
#     hython_path, hkey_path = locate_hython_and_hkey()
#     subprocess.Popen([hkey_path])
#     subprocess.call([hython_path, "main.py"] + argv)# "syntheticDataGen_001.hip", "main.py"] + argv)

# bootstrap(sys.argv[1:])