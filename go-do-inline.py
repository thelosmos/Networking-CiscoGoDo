# Import Libraries
import paramiko
import re
import getpass
import time
import sys
import re

# Disable paging
def DISABLE_PAGING(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

if __name__ == '__main__':
    # Login prompt
    ip = sys.argv[1]
    username = input("Username:")
    password = getpass.getpass("User Password:")
    enablePassword = getpass.getpass("Enable Password:")
    command = sys.argv[2]

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    
    # Initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    remote_conn = remote_conn_pre.invoke_shell()
    print("Interactive SSH Connection Established to %s" % ip)

    # Enter privileged exec mode
    output = remote_conn.recv(1000000)
    outputStr = output.decode('utf-8')
    if (outputStr.endswith('#')):
        print("In privileged mode.")
    else:
        print("Attepting to enter privileged mode.")
        remote_conn.send("enable")
        remote_conn.send("\n")
        remote_conn.send(enablePassword)
    
    # Show current prompt
    print(outputStr)

    # Disable paging
    DISABLE_PAGING(remote_conn)

    # Send command
    remote_conn.send(command)
    remote_conn.send("\n")
    time.sleep(2)
    output = remote_conn.recv(1000000)
    outputStr = output.decode('utf-8')
    
    # Show command result
    print(outputStr)