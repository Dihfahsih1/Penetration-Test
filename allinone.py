import os

a='''
Welcome to PTF 
Select an option you want to run:
1) Port Scanning.
2) Network sniffing and store in pcap file.
3) Crack password using John the Ripper.
4) Collect Email/banner/urls from a URL.
5) Vulnerability scan.
6) Display running services on a host.
'''
print (a)

num = int(input("Enter your option: "))



if num == 1:
    print("What type of Scan you want to do?..")
    print("1) SYN   2) Xmas   3) Fin")
    option=int(input("Enter your choice: "))
    RHOST = input("Enter the RHOST: ")
    if option ==1:
        print('Please wait for the process to complete')
        syn=os.system("nmap -sS " + RHOST)
        print(syn)
        print("Process complete")
    elif option == 2:
        print('Please wait for the process to complete')
        Xmas=os.system("nmap -sX " + RHOST)
        print(Xmas)
        print("Process complete")
    elif option ==3:
        print('Please wait for the process to complete')
        Fin=os.system("nmap -sF " + RHOST)
        print(Fin)
        print("Process complete")
    else:
        print("Wrong input")        

    
elif num == 2:
    interface = input("Enter the interface: ")
    time = input("Enter the duration in seconds: ")
    filename = input("Enter the filename to save as: ")
    print('Please wait for the process to complete')
    shark = os.system("tshark -i " + interface + " -a duration:" + time + " -w " + filename + ".pcap")
    print(shark)
    print("file saved in your home directory")
  
elif num == 3:
    wordlist = input("Enter the wordlist directory: ")
    md5_hashes_file = input("Enter the directory of the file containing the md5 hashes: ")
    print('Please wait for the process to complete')
    jhonny = os.system("john --format=raw-md5 --wordlist " + wordlist + " " + md5_hashes_file )
    print(jhonny)

elif num == 6:
    RHOST = input("Enter the RHOST: ")
    print('Please wait for the process to complete')
    exe1= os.system("nmap -sV " + RHOST )
    print(exe1)

elif num == 5:
    RHOST = input("Enter the RHOST: ")
    print('Please wait for the process to complete')
    exe2= os.system("nmap -sV -script=vulners.nse " + RHOST )
    print(exe2)    

elif num == 4:
    url = input("Enter the url: ")
    print('Please wait for the process to complete')
    osint= os.system("theHarvester -d " + url + " -l 1000 -b all")
    print(osint)    

else:
    print("Wrong input")   