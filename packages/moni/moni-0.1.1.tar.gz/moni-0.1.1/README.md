# moni

moni 是一个查看多 numa 系统信息的工具, htop/numactl/numastatus/ps 等等现有工具可以做到类似的事情, 但是还需要做一些参数和管道处理. moni 希望使用一个简单易用的方式查看系统信息

## 功能

查看每个numa节点的内存和 CPU 的使用情况

```bash
moni numa
```

查看当前系统中使用 CPU 最高的 5 个进程

```bash
moni cpu
```

查看系统中使用内存最多的前 5 个进程

```bash
moni mem
```

查看最近使用 sudo 的五个命令, 包括用户名, 完整命令名

```bash
moni cmd
```

查看某一个用户最近使用的 5 条命令, 如果用户不是你则需要 sudo 权限

```bash
moni cmd <user-name>
```

查看当前系统中所有用户的登录情况,包括登录时间、登录IP

```bash
moni login
```

如何查看当前系统中某个用户的登录情况,包括登录时间、登录地点

```bash
moni login <user-name>
```

## 下载

```bash
sudo apt install moni
```

或者

```bash
cargo install moni
```

## 参考

- 软件包发布
  - [ubuntu packages](https://packages.ubuntu.com/)
  - [debian packages](https://packages.debian.org/)
  - [archlinux packages](https://archlinux.org/packages/)
  - [archlinux aur](https://aur.archlinux.org/)
  - [fedoraproject packages](https://packages.fedoraproject.org/)
  - [opensuse software](https://software.opensuse.org/search)