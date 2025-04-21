# alibaba-cloud-ops-mcp-server

## 准备

安装[uv](https://github.com/astral-sh/uv)

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 启动方式

本地开发环境启动

```bash
ALIBABA_CLOUD_ACCESS_KEY_ID=<你的AK> ALIBABA_CLOUD_ACCESS_KEY_SECRET=<你的SK> uv run src/alibaba_cloud_ops_mcp_server/server.py --transport sse
```

安装包启动

```bash
ALIBABA_CLOUD_ACCESS_KEY_ID=<你的AK> ALIBABA_CLOUD_ACCESS_KEY_SECRET=<你的SK> uvx alibaba-cloud-ops-mcp-server@latest --transport sse
```

## 调试

使用 [VS Code](https://code.visualstudio.com/) + [Cline](https://cline.bot/) 配置MCP Server

## 功能点（Tool）

| **产品** | **工具** | **功能** | **实现方式** | **状态** |
| --- | --- | --- | --- | --- |
| ECS | RunCommand | 运行命令 | OOS | Done |
|  | StartInstances | 启动实例 | OOS | Done |
|  | StopInstances | 停止实例 | OOS | Done |
|  | RebootInstances | 重启实例 | OOS | Done |
|  | DescribeInstances | 查看实例 | API | Done |
|  | DescribeRegions | 查看地域 | API | Done |
|  | DescribeZones | 查看可用区 | API | Done |
|  | DescribeAvailableResource | 查看资源库存 | API | Done |
|  | DescribeImages | 查看镜像 | API | Done |
|  | DescribeSecurityGroups | 查看安全组 | API | Done |
|  | RunInstances | 创建实例 | OOS | Done |
|  | DeleteInstances | 删除实例 | API | Done |
|  | ResetPassword | 修改密码 | OOS | Done |
|  | ReplaceSystemDisk | 更换操作系统 | OOS | Done |
| VPC | DescribeVpcs | 查看VPC | API | Done |
|  | DescribeVSwitches | 查看VSwitch | API | Done |
| CloudMonitor | GetCpuUsageData | 获取ECS实例的CPU使用率数据 | API | Done |
|  | GetCpuLoadavgData | 获取CPU一分钟平均负载指标数据 | API | Done |
|  | GetCpuloadavg5mData | 获取CPU五分钟平均负载指标数据 | API | Done |
|  | GetCpuloadavg15mData | 获取CPU十五分钟平均负载指标数据 | API | Done |
|  | GetMemUsedData | 获取内存使用量指标数据 | API | Done |
|  | GetMemUsageData | 获取内存利用率指标数据 | API | Done |
|  | GetDiskUsageData | 获取磁盘利用率指标数据 | API | Done |
|  | GetDiskTotalData | 获取磁盘分区总容量指标数据 | API | Done |
|  | GetDiskUsedData | 获取磁盘分区使用量指标数据 | API | Done |