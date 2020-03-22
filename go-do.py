# Import Libraries
import paramiko
import re
import getpass
import time

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
    print(
    '''
    ######################################################################
    ### Please enter in connection information and command to be used. ###
    ######################################################################
    '''
        )
    ip = input("Layer 3 Device IP:")
    username = input("Username:")
    password = getpass.getpass("User Password:")
    enablePassword = getpass.getpass("Enable Password:")
    command = input("Command:")

     # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    
    # Initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    remote_conn = remote_conn_pre.invoke_shell()
    print("Interactive SSH Connection Established to %s" % ip)

    # Show current prompt
    output = remote_conn.recv(1000000)
    outputStr = output.decode('utf-8')
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