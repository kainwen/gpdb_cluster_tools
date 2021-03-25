## Host Init

[https://gpdb.docs.pivotal.io/6-15/install\_guide/prep\_os.html](https://gpdb.docs.pivotal.io/6-15/install\_guide/prep\_os.html)

1. use `ssh-copy-id` to set ssh without password
2. use `visudo` to gpadmin
3. Each host generate ssh-key: `ssh-keygen`
4. disk io read-ahead, change root's crontab: `@reboot  /sbin/blockdev --setra 16384 /dev/???`
5. Disable Transparent Huge Pages: ` sudo apt install libhugetlbfs-bin; sudo hugeadm --thp-never`
6. XFS mount parameter: `rw,nodev,noatime,inode64`, like `/dev/data /data xfs nodev,noatime,nobarrier,inode64 0 0
`