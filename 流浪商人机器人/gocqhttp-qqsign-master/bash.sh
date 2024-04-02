#!/bin/bash

# 添加颜色变量
RED="\e[31m"           # 红色
GREEN="\e[32m"         # 绿色
YELLOW="\e[33m"        # 黄色
RESET="\e[0m"          # 重置颜色

# 添加常量
QSIGN_VERSION="1.1.9"

# 添加函数以显示不同颜色的消息
print_message() {
    local message="$1"
    local color="$2"
    echo -e "${color}${message}${RESET}"
}

# 定义协议内容
protocol="

一键构建qsign环境启动qsign
                    _      _ __
   ___    __ __    (_)    | '_ \
  (_-<    \ V /    | |    | .__/
  /__/_   _\_/_   _|_|_   |_|

"
print_message "$protocol" "$YELLOW"

sleep 1

# 检查是否具有 root 权限
if [ "$(whoami)" != "root" ]; then
    print_message "请使用 root 权限执行本脚本！" "$RED"
    exit 1
fi

print_message "正在下载并检查所需软件包，请稍等..." "$GREEN"

sleep 1

# 函数：安装软件包
install_package() {
    local package_name="$1"
    local message="$2"

    if ! command -v "$package_name" &> /dev/null; then
        print_message "$message" "$YELLOW"

        if command -v apt &> /dev/null; then
            apt install -y "$package_name" > /dev/null
        elif command -v apt-get &> /dev/null; then
            apt-get install -y "$package_name" > /dev/null
        elif command -v dnf &> /dev/null; then
            dnf install -y "$package_name" > /dev/null
        elif command -v yum &> /dev/null; then
            yum install -y "$package_name" > /dev/null
        elif command -v pacman &> /dev/null; then
            pacman -Syu --noconfirm "$package_name" > /dev/null
        else
            print_message "无法确定操作系统的包管理器，请手动安装软件包 $package_name" "$RED"
            exit 1
        fi
        print_message "$package_name 工具安装完成" "$GREEN"
    else
        print_message "已安装 $package_name 工具，跳过安装" "$GREEN"
    fi
}

# 检查并安装 pv
install_package "pv" "未检测到 pv 工具，开始安装..."

sleep 1

# 检查并安装 unzip
install_package "unzip" "未检测到 unzip 工具，开始安装..."

sleep 1

# 检查是否安装 jdk
if ! command -v java &> /dev/null; then
    print_message "未检测到 Java 环境，开始安装 JDK..." "$YELLOW"

    if command -v apt &> /dev/null; then
        apt update > /dev/null
        apt install -y openjdk-11-jdk > /dev/null
    elif command -v apt-get &> /dev/null; then
        apt-get update > /dev/null
        apt-get install -y openjdk-11-jdk > /dev/null
    elif command -v dnf &> /dev/null; then
        dnf update -y > /dev/null
        dnf install -y java-11-openjdk-devel > /dev/null
    elif command -v yum &> /dev/null; then
        yum update -y > /dev/null
        yum install -y java-11-openjdk-devel > /dev/null
    elif command -v pacman &> /dev/null; then
        pacman -Syu --noconfirm jdk11-openjdk > /dev/null
    else
        print_message "无法确定操作系统的包管理器，请手动安装 Java JDK" "$RED"
        exit 1
    fi
    print_message "Java JDK 环境安装完成" "$GREEN"
else
    print_message "已安装 Java 环境，跳过安装" "$GREEN"
fi

sleep 1

# 如果非第一次启动
if [ -d "unidbg-fetch-qsign-$QSIGN_VERSION" ]; then
    options=("启动 qsign_operations.sh" "重新配置 unidbg-fetch-qsign" "退出脚本")

    PS3="发现已有目录 unidbg-fetch-qsign-$QSIGN_VERSION，请选择操作: "
    select choice in "${options[@]}"; do
        case $choice in
            "启动 qsign_operations.sh")
                if [ -f "unidbg-fetch-qsign-$QSIGN_VERSION/qsign_operations.sh" ]; then
                    cd "unidbg-fetch-qsign-$QSIGN_VERSION"
                    ./qsign_operations.sh
                    exit
                else
                    print_message "文件 qsign_operations.sh 不存在，请重新配置（若是 nohup 管理请直接使用 nohup 命令）" "$RED"
                    exit 1
                fi
                ;;
            "退出脚本")
                print_message "已退出脚本，Have a Fun!" "$RED"
                exit 0
                break
                ;;
            *)
                print_message "输入错误，无效的选择！" "$RED"
                ;;
        esac
    done
fi

sleep 1

# 查找 Java 路径并设置 JAVA_HOME
java_path=$(readlink -f $(which java))
if [ -n "$java_path" ]; then
    java_home=$(dirname $(dirname "$java_path"))
    export JAVA_HOME="$java_home"
    print_message "已设置 JAVA_HOME 为：$JAVA_HOME" "$GREEN"
else
    print_message "未找到 Java 安装路径，等待程序自动识别" "$YELLOW"
fi

sleep 1

# 进入解压后的文件夹
cd "unidbg-fetch-qsign-$QSIGN_VERSION"

# 检查 8080 端口是否被占用
if netstat -tuln | grep ":8080" > /dev/null; then
    print_message "默认端口 8080 已被占用，请自行前往 txlib/<协议版本>/config.json 修改端口号（若已修改可无视本提示）" "$RED"
else
    print_message "默认端口 8080 未被占用" "$GREEN"
fi

# 检查系统是否有 systemd 服务
systemd_check="$(ps -p 1 -o comm=)"
if [[ "${systemd_check}" != "systemd" ]]; then
    # 如果系统中没有 systemd 服务，则使用 nohup 进行管理
    print_message "当前系统中没有 systemd 服务，尝试使用 nohup 进行管理" "$YELLOW"

    # 读取 txlib 文件夹下的子文件夹名称
    txlib_folders=($(ls -d txlib/*/))

    # 让用户选择协议版本
    print_message "请选择协议版本：" "$GREEN"
    for ((i=0; i<${#txlib_folders[@]}; i++)); do
        folder_name=$(basename "${txlib_folders[$i]}")  # 获取文件夹名称，不包含 "txlib"
        print_message "$((i+1)): $folder_name" "$GREEN"
    done

    read -p "输入选择的协议版本数字: " version_choice

    # 验证用户输入是否有效
    if [[ ! "$version_choice" =~ ^[0-9]+$ || "$version_choice" -lt 1 || "$version_choice" -gt ${#txlib_folders[@]} ]]; then
        print_message "无效的选择，请输入有效的协议版本数字" "$RED"
        exit 1
    fi

    # 获取用户选择的协议版本
    selected_version=$(basename "${txlib_folders[$((version_choice-1))]}")

    print_message "已选择协议版本: $selected_version" "$GREEN"

    # 创建一个新的 nohup 任务并运行命令
    nohup bash bin/unidbg-fetch-qsign --basePath=txlib/$selected_version > qsign.log 2>&1 &

    # 获取 nohup 任务的 PID
    qsign_pid=$!

    # 显示 nohup 任务的 PID
    print_message "已创建 nohup 任务并运行命令，PID 为: $qsign_pid" "$GREEN"

    # 循环检测进程是否存活，如果进程丢失了就再启动一个
    while true; do
        if ! kill -0 $qsign_pid 2>/dev/null; then
            # 进程不存在，重新启动
            nohup bash bin/unidbg-fetch-qsign --basePath=txlib/$selected_version > qsign.log 2>&1 &
            qsign_pid=$!
            print_message "进程已丢失，已重新启动，新的PID为: $qsign_pid" "$RED"
        fi
        # 每隔一段时间检测一次，可以根据需要调整 sleep 的时间
        sleep 1
    done

else
    # 如果系统有 systemd 服务
    print_message "当前系统中存在 systemd 服务" "$GREEN"

    # 给予脚本执行权限
    chmod +x "qsign_operations.sh"

    print_message "给予脚本qsign_operations执行权限成功，5 秒钟后启动..." "$GREEN"

    sleep 5

    # 运行脚本
    ./qsign_operations.sh
fi