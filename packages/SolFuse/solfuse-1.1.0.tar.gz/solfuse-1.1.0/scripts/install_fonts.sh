#!/bin/bash

# 安装常用的中文字体
echo "开始安装中文字体..."

# 检测操作系统
if [ -f /etc/lsb-release ] || [ -f /etc/debian_version ]; then
    # Debian/Ubuntu系统
    sudo apt-get update
    sudo apt-get install -y fonts-wqy-microhei fonts-wqy-zenhei fonts-noto-cjk
elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL/Fedora系统
    sudo yum install -y wqy-microhei-fonts wqy-zenhei-fonts google-noto-cjk-fonts
elif [ -f /etc/arch-release ]; then
    # Arch Linux系统
    sudo pacman -S --noconfirm wqy-microhei wqy-zenhei noto-fonts-cjk
elif [ -f /etc/SuSE-release ] || [ -f /etc/SUSE-brand ]; then
    # SUSE系统
    sudo zypper install -y wqy-microhei-fonts wqy-zenhei-fonts google-noto-cjk-fonts
else
    echo "无法识别的Linux系统，请手动安装中文字体"
fi

# 更新字体缓存
fc-cache -fv

# 检查是否安装成功
echo "已安装的中文字体:"
fc-list :lang=zh-cn

echo "字体安装完成"

# 创建matplotlib配置目录(如果不存在)
MATPLOTLIB_CONFIG_DIR=~/.config/matplotlib
mkdir -p $MATPLOTLIB_CONFIG_DIR

# 创建matplotlibrc文件并配置中文字体
cat > $MATPLOTLIB_CONFIG_DIR/matplotlibrc << EOF
font.family         : sans-serif
font.sans-serif     : WenQuanYi Micro Hei, WenQuanYi Zen Hei, Noto Sans CJK SC, SimHei, Microsoft YaHei, Arial Unicode MS, sans-serif
axes.unicode_minus  : False
EOF

echo "matplotlib中文字体配置完成"
