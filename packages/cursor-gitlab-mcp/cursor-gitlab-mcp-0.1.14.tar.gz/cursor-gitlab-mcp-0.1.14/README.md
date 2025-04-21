# GitLab MCP 服务

这是一个基于Python实现的GitLab MCP（Model Control Protocol）服务，用于在Cursor IDE中提供GitLab操作支持。

## 项目目标

- 提供自然语言到Git操作的转换
- 支持内网GitLab的代码管理
- 实现安全的Git操作控制
- 提供可扩展的CI/CD集成能力

## 系统架构

```
用户指令 → Cursor客户端 → MCP服务端 → GitLab API → 执行Git操作
```

### 核心模块

1. **环境配置模块**
   - 虚拟环境管理
   - 依赖包管理
   - 配置文件管理

2. **GitLab连接模块**
   - GitLab API封装
   - 认证管理
   - 错误处理

3. **MCP服务端**
   - 命令解析
   - 操作执行
   - 结果返回

4. **自然语言处理层**
   - 指令映射
   - 参数解析
   - 默认行为

### 安全控制

- 访问控制：基于白名单的路径控制
- 操作审计：完整的操作日志记录
- 环境隔离：Docker容器化部署
- 权限管理：基于角色的命令限制

## 安装

你可以通过pip直接安装gitlab-mcp：

```bash
pip install gitlab-mcp
```

或者使用国内镜像源安装：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gitlab-mcp
```

## 快速开始

### 安装步骤

1. 在Cursor IDE中打开设置
2. 找到MCP配置部分
3. 将以下配置复制到配置文件中：
```json
{
  "mcpServers": {
    "gitlab": {
      "command": "mcp-gitlab",
      "env": {
        "GITLAB_API_BASE": "http://your-gitlab-server.com",
        "GITLAB_ACCESS_TOKEN": "your-access-token"
      }
    }
  }
}
```

4. 修改配置中的`GITLAB_API_BASE`和`GITLAB_ACCESS_TOKEN`为你的GitLab信息

## 支持的命令

### 基础Git操作
- `查看状态` - 查看当前仓库状态
- `更新代码` - 拉取最新代码
- `提交修改` - 提交代码修改
- `推送代码` - 推送代码到远程
- `创建分支` - 创建并切换到新分支
- `切换分支` - 切换到指定分支
- `删除分支` - 删除本地分支
- `删除远程分支` - 删除远程分支
- `查看日志` - 查看提交历史
- `查看文件历史` - 查看指定文件的修改历史
- `查看差异` - 查看工作区和暂存区的差异
- `暂存修改` - 将修改添加到暂存区
- `撤销修改` - 撤销工作区的修改

### GitLab操作
- `查看项目提交记录` - 查看指定项目的提交记录
- `列出项目分支` - 查看项目分支
- `创建合并请求` - 创建合并请求
- `查看合并请求` - 查看项目的合并请求列表
- `查看项目成员` - 查看项目成员列表
- `查看项目标签` - 查看项目标签列表
- `创建项目标签` - 创建项目标签
- `查看项目文件` - 查看项目文件列表
- `查看文件内容` - 查看项目文件内容
- `搜索项目` - 搜索GitLab项目
- `查看项目统计` - 查看项目统计信息
- `查看分支保护` - 查看分支保护设置
- `设置分支保护` - 设置分支保护规则

## 获取帮助

如果遇到问题，请检查：
1. GitLab服务器地址是否正确
2. 访问令牌是否有足够权限

## 开发指南

### 发布新版本

1. 更新版本号
   - 在`setup.py`中更新`version`
   - 在`CHANGELOG.md`中添加新版本说明

2. 构建发布包
```bash
# 安装构建工具（使用国内镜像源）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple twine wheel

# 运行发布脚本
./release.sh
```

3. 发布到PyPI
   - 确保已安装twine
   - 运行发布脚本
   - 输入PyPI账号密码

### 开发环境设置

1. 克隆项目
```bash
git clone https://github.com/yourusername/gitlab-mcp.git
cd gitlab-mcp
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 安装开发依赖（使用国内镜像源）
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e .
```

## 国内镜像源

如果遇到网络问题，可以使用以下国内镜像源：

1. 清华大学镜像源（推荐）
```
https://pypi.tuna.tsinghua.edu.cn/simple
```

2. 阿里云镜像源
```
https://mirrors.aliyun.com/pypi/simple/
```

3. 中国科技大学镜像源
```
https://pypi.mirrors.ustc.edu.cn/simple/
```

4. 豆瓣镜像源
```
https://pypi.douban.com/simple/
```

使用方法：
```bash
# 临时使用
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple package_name

# 永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 许可证

MIT License 

## 版本更新记录

### v0.1.7 (2024-03-21)
- 完善了项目文档
- 优化了包的构建和发布流程
- 更新了依赖包版本
- 修复了已知问题

### v0.1.6 及更早版本
- 实现了基础的GitLab操作功能
- 添加了命令行工具支持
- 集成了GitLab API
- 建立了基础项目结构 