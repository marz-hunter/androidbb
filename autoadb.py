import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())
    return stdout.decode().strip()

def list_devices():
    run_command("adb devices")

def open_powershell_and_run(command):
    powershell_command = f'powershell -Command "{command}"'
    process = subprocess.Popen(powershell_command, shell=True)
    return process

def main():
    while True:
        list_devices()
        
        ip_port = input("Masukkan ip:port dari device: ")
        adb_shell_command = f'adb -s {ip_port} shell'
        
        print("Membuka adb shell dan menjalankan frida-server...")
        open_powershell_and_run(f'{adb_shell_command} "/data/local/tmp/frida-server"')

        frida_ps_command = f'frida-ps -D {ip_port} -ai'
        print("Menjalankan frida-ps untuk mendapatkan list paket aplikasi yang terinstall...")
        open_powershell_and_run(frida_ps_command)
        
        package_name = input("Masukkan nama paket aplikasi: ")
        pid_command = f'adb -s {ip_port} shell pidof {package_name}'
        
        print("Mendapatkan PID dari aplikasi...")
        pid = run_command(pid_command)
        
        if pid:
            frida_command = f'frida -D {ip_port} -l SSL-BYE.js -p {pid}'
            print("Menjalankan Frida dengan skrip SSL-BYE.js...")
            open_powershell_and_run(frida_command)
        else:
            print(f"Tidak dapat menemukan PID untuk paket {package_name}")

        another_device = input("Apakah ingin menjalankan perintah untuk device lain? (y/n): ")
        if another_device.lower() != 'y':
            break

if __name__ == "__main__":
    main()
