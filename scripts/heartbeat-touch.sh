#!/bin/bash
# 思行心跳——守护进程读取此文件判断主实例是否存活
date -u +%s > /root/workspace/data/.sx_heartbeat
