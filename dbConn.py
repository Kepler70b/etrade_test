import os
import shlex
import subprocess

def getCreds(dbInfo,catdbinst):
    try:
        application=os.environ['APPLICATION']
        env=os.environ['ENV']
        serverName=dbInfo['serverName']
        dbName=dbInfo['dbName']
    except KeyError as e:
        print(f"Missing environment variable: {e}")
        return None
    try:
        virtualName=f"{application}-{env}-{serverName}-{dbName}"
        cat_cyberark_cmd = f"/opt/CyberArk/CyberArkCLI/cyberarkcli getpassword -p {catdbinst} -v {virtualName} --output json"
        args = shlex.split(cat_cyberark_cmd)
        result = subprocess.run(args, check=True, text=True, capture_output=True)
        tempCred=result.stdout.strip()
        cyber_ark_creds=tempCred.split(',')

        return cyber_ark_creds
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None
