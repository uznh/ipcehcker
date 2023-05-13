import socket
import sys
from colorama import init,Fore
from multiprocessing import Pool

red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
cyan = Fore.LIGHTCYAN_EX
rest = Fore.RESET

def scan(ip,port):
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip,port))
        if str(result) == '0':
            print(f'{yellow}{ip} {rest}==> {green}Live Port:{green}{port}')
            with open('LiveIps.txt','a') as out:
                out.write(ip+'\n')
                out.close()
        else:
            print(f'{yellow}{ip} {rest}==> {red}Closed Port:{green}{port}')
    except Exception as e:
        print('Error Occurred  ',e)
    

banner = f'''
{yellow}
██████╗  ██████╗ ██████╗ ████████╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝   ██║       ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██╔═══╝ ██║   ██║██╔══██╗   ██║       ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║     ╚██████╔╝██║  ██║   ██║       ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                  {green}        By @K6510  https://facebook.com/Said.Hacke                                                                     
'''
if __name__ == '__main__':
    init(autoreset=True)
    print(banner)
    file_name = input("{}Enter Your List:\n".format(cyan)).replace(".txt","")
    port = int(input("{}Enter Port Number:\n".format(yellow)))
    
    try:
        with open(f'{file_name}.txt','r') as f:
            list_name = f.readlines()

        pool = Pool(50)
        results = []
        for site in list_name:
            site = site.rstrip()
            result = pool.apply_async(scan, args=(site, port))
            results.append(result)

        # Wait for all tasks to complete
        pool.close()
        pool.join()


        # Check if any errors occurred during scanning
        for result in results:
            if result.get() is not None:
                print('An error occurred during scanning.')

        print('** Finished **')
        sys.exit(0)

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        sys.exit(1)
    except FileNotFoundError:
        print('{} Not Found'.format(file_name))
