RLIMIT = """
* soft nofile 524288
* hard nofile 524288
* soft nproc 131072
* hard nproc 131072
"""

if __name__ == "__main__":
    with open("/etc/security/limits.conf", "w") as f:
        print(RLIMIT, file=f)
