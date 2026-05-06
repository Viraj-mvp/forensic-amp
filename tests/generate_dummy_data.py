import os

def generate_log():
    content = """192.168.1.10 - - [04/Jan/2026:10:00:00 +0000] "GET /index.php HTTP/1.1" 200 1024
192.168.1.11 - - [04/Jan/2026:10:01:00 +0000] "GET /login.php?user=admin' OR 1=1-- HTTP/1.1" 200 512
10.0.0.5 - - [04/Jan/2026:10:02:00 +0000] "POST /upload.php HTTP/1.1" 500 0
192.168.1.12 - - [04/Jan/2026:10:03:00 +0000] "GET /?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E HTTP/1.1" 200 2048
"""
    with open("tests/dummy.log", "w") as f:
        f.write(content)
    print("Dummy log created at tests/dummy.log")

if __name__ == "__main__":
    generate_log()
