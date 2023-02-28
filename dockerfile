FROM python

USER root

ENV RUN_PATH /root/personal_python_project/

WORKDIR $RUN_PATH

COPY . $RUN_PATH

ADD sources.list /etc/apt

#RUN ["touch /etc/apt/sources.list","echo -e 'deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free \n # deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free\n deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free\n # deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free\n deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free\n # deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free\n deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free\n # deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free' > /etc/apt/sources.list","apt-get update"]

RUN more /etc/apt/sources.list

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&  \
    echo 'Asia/Shanghai' >/etc/timezone &&\
    echo "started" && \
    apt-get update && \
    apt-get upgrade -y

RUN apt-get install build-essential -y && \
    apt-get install manpages-dev -y && \
    gcc --version

# 安装 python 环境,配置pip源，导入所有依赖, 并且启动这个项目即可
RUN cd $RUN_PATH && \
    pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple && \
    pip install -r ./requirements.txt

EXPOSE 9528

CMD ["python","run.py"]


#tee /etc/apt/sources.list << EOF
## 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
#deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
## deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
#deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
## deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
#
#deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
## deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
#
#deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
## deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
#EOF
