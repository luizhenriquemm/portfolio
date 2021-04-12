#Versao 1.1
import psutil
import time
import requests
import datetime
import platform

nome_computador = "SERVER-1"

print ("Sistema de monitoramento de servidores")
print ("Não feche este aplicativo!")
print ("Computador: " + nome_computador)

while (True):
    os = str(platform.system()) + " " +  str(platform.release())
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    cpu_uso = psutil.cpu_percent(interval=0.5, percpu=True)
    cpu_frequencia = float(psutil.cpu_freq().current)

    memoria_uso = float(psutil.virtual_memory().percent)
    memoria_total = round(float(psutil.virtual_memory().total) / (1024 * 1024 * 1024), 2)

    discos = []
    discos_tamanho = []
    discos_uso = []
    discos_formato = []
    for valor in psutil.disk_partitions():
        if valor.device[0:9] != "/dev/loop":

            discos.append(valor.device)
            
            if str(valor.opts) != "cdrom":
                discos_uso.append(psutil.disk_usage(valor.mountpoint).percent)
                discos_tamanho.append(round(float(psutil.disk_usage(valor.mountpoint).total) / (1024 * 1024 * 1024), 2))
                discos_formato.append(valor.fstype)
            else:
                discos_uso.append("null")
                discos_tamanho.append("null")
                discos_formato.append("CDROM")
  
    interfaces = []
    interfaces_ips = []
    for nic, addrs in psutil.net_if_addrs().items():
        if nic != "Loopback Pseudo-Interface 1" and nic != "lo":
            for addr in addrs:
                if str(addr.family) == "AddressFamily.AF_INET":
                    interfaces.append(nic)
                    interfaces_ips.append(addr.address)

    r = requests.post("http://10.1.1.242/modules/gestor-ti/receiver.php", data={'nome': str(nome_computador), 'os': str(os), 'cpu_uso': str(cpu_uso), 'cpu_frequencia': str(cpu_frequencia), 'memoria_uso': str(memoria_uso), 'memoria_total': str(memoria_total), 'discos_total': len(discos), 'discos': str(discos), 'discos_tamanho': str(discos_tamanho), 'discos_formato': str(discos_formato), 'discos_uso': str(discos_uso), 'interfaces': str(interfaces), 'interfaces_ip': str(interfaces_ips), 'boot_time': str(boot_time)})

    if str(r.text) != "sucesso":
        print (r.text)
    
    time.sleep(1)
