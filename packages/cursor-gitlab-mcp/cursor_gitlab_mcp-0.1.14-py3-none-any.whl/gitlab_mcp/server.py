"""
MCP服务端实现 - 处理Git和GitLab操作命令
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import typer
from datetime import datetime
import gitlab
import urllib3
import re
from mcp.server.fastmcp import FastMCP
from .connector import GitLabConnector

# 配置日志目录
log_dir = os.path.join(str(Path.home()), '.local', 'share', 'gitlab_mcp')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'gitlab_mcp.log')

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('gitlab_mcp')

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = typer.Typer()
mcp = FastMCP("gitlab")

try:
    # 初始化GitLab连接器
    gitlab_connector = GitLabConnector()
    logger.info("GitLab连接器初始化成功")
except Exception as e:
    logger.error(f"GitLab连接器初始化失败: {str(e)}")
    gitlab_connector = None

# 命令映射表
COMMAND_MAP = {
    "更新代码": {"command": "pull", "args": []},
    "提交修改": {"command": "commit", "args": []},  # 移除固定的commit message
    "推送代码": {"command": "push", "args": []},
    "查看状态": {"command": "status", "args": ["-s"]},
    "创建分支": {"command": "checkout", "args": ["-b"]},
    "切换分支": {"command": "checkout", "args": []},
    "克隆项目": {"command": "clone", "args": []},
    "查看项目": {"command": "list_projects", "args": []},
    "项目列表": {"command": "list_projects", "args": []},
    "我的项目": {"command": "list_projects", "args": []},
    "所有项目": {"command": "list_projects", "args": []},
    "查看分支": {"command": "list_project_branches", "args": []},
    "分支列表": {"command": "list_project_branches", "args": []},
    "最近提交": {"command": "check_collection_commits", "args": []}
}

def format_date(date_str: str) -> str:
    """格式化日期字符串"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.error(f"日期格式化错误: {str(e)}")
        return date_str

def generate_commit_message(repo_path: str) -> str:
    """
    根据Git状态自动生成提交信息
    
    Args:
        repo_path: 仓库路径
        
    Returns:
        生成的提交信息
    """
    try:
        # 获取修改的文件列表
        status_cmd = ["git", "-C", repo_path, "status", "--porcelain"]
        result = subprocess.run(status_cmd, capture_output=True, text=True, check=True)
        
        changes = result.stdout.strip().split('\n')
        if not changes or changes[0] == '':
            return "no changes"
            
        # 分析变更
        added = []
        modified = []
        deleted = []
        
        for change in changes:
            if not change:
                continue
            status = change[:2]
            file = change[3:]
            
            if status.startswith('A'):
                added.append(file)
            elif status.startswith('M'):
                modified.append(file)
            elif status.startswith('D'):
                deleted.append(file)
                
        # 生成提交信息
        message_parts = []
        
        if added:
            message_parts.append(f"新增: {', '.join(added)}")
        if modified:
            message_parts.append(f"修改: {', '.join(modified)}")
        if deleted:
            message_parts.append(f"删除: {', '.join(deleted)}")
            
        return " | ".join(message_parts)
        
    except Exception as e:
        logger.error(f"生成提交信息时出错: {str(e)}")
        return "自动提交"

def parse_command(text: str) -> Dict[str, Any]:
    """
    将自然语言转换为Git命令
    
    Args:
        text: 用户输入的自然语言命令
        
    Returns:
        包含命令和参数的字典
    """
    logger.debug(f"解析命令: {text}")
    
    # 处理克隆项目命令
    clone_match = re.search(r'克隆[项目仓库]*\s*[\"\'](.*?)[\"\']', text)
    if clone_match:
        project_url = clone_match.group(1)
        return {"command": "clone", "args": [project_url]}
    
    # 处理项目相关的自然语言查询
    if any(keyword in text.lower() for keyword in ["项目", "仓库", "代码库"]):
        if any(keyword in text.lower() for keyword in ["列表", "所有", "我的"]):
            return {"command": "list_projects", "args": []}
        elif any(keyword in text.lower() for keyword in ["分支", "分支列表"]):
            return {"command": "list_project_branches", "args": []}
        elif any(keyword in text.lower() for keyword in ["提交", "最近提交"]):
            return {"command": "check_collection_commits", "args": []}
    
    # 处理其他命令
    for keyword, cmd in COMMAND_MAP.items():
        if keyword in text:
            logger.debug(f"找到匹配命令: {cmd}")
            # 如果是提交命令，不返回args，让后续代码处理
            if cmd["command"] == "commit":
                return {"command": "commit", "args": []}
            return cmd
            
    logger.warning(f"未找到匹配命令，使用默认状态命令")
    return {"command": "status", "args": []}  # 默认操作

@mcp.tool()
def git_operation(
    repo_path: str,
    command: str = typer.Option(..., help="支持clone/pull/push/status/checkout等操作")
) -> str:
    """
    执行Git操作
    
    Args:
        repo_path: 仓库路径
        command: Git命令
        
    Returns:
        命令执行结果
    """
    logger.info(f"执行Git操作: {command} 在路径: {repo_path}")
    
    try:
        # 解析命令
        cmd_info = parse_command(command)
        
        # 处理克隆命令
        if cmd_info["command"] == "clone":
            if not cmd_info["args"]:
                return "错误：克隆命令需要提供项目URL"
                
            project_url = cmd_info["args"][0]
            logger.info(f"克隆项目: {project_url} 到 {repo_path}")
            
            # 如果目录不存在，创建它
            os.makedirs(repo_path, exist_ok=True)
            
            # 执行克隆命令
            clone_cmd = ["git", "clone", project_url, repo_path]
            result = subprocess.run(clone_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return f"成功克隆项目到: {repo_path}"
            else:
                return f"克隆失败: {result.stderr}"
        
        # 对于其他命令，检查路径是否存在
        if not os.path.exists(repo_path):
            error_msg = f"错误：路径 {repo_path} 不存在"
            logger.error(error_msg)
            return error_msg
            
        # 检查是否是Git仓库
        git_dir = os.path.join(repo_path, '.git')
        if not os.path.exists(git_dir):
            error_msg = f"错误：{repo_path} 不是Git仓库"
            logger.error(error_msg)
            return error_msg
            
        # 特殊处理提交命令
        if cmd_info["command"] == "commit":
            # 生成提交信息
            commit_message = generate_commit_message(repo_path)
            if commit_message == "no changes":
                return "没有需要提交的更改"
                
            cmd_info["args"] = ["-m", commit_message]
            
            # 自动添加所有更改
            add_cmd = ["git", "-C", repo_path, "add", "."]
            subprocess.run(add_cmd, check=True)
        
        # 执行Git命令
        git_cmd = ["git", "-C", repo_path, cmd_info["command"]] + cmd_info["args"]
        logger.debug(f"执行命令: {' '.join(git_cmd)}")
        
        result = subprocess.run(git_cmd, capture_output=True, text=True, check=True)
        
        # 如果是提交命令，自动推送
        if cmd_info["command"] == "commit" and result.returncode == 0:
            logger.info("提交成功，准备推送代码...")
            push_cmd = ["git", "-C", repo_path, "push"]
            push_result = subprocess.run(push_cmd, capture_output=True, text=True)
            
            if push_result.returncode == 0:
                return f"提交并推送成功:\n{result.stdout}\n推送结果:\n{push_result.stdout}"
            else:
                return f"提交成功但推送失败:\n{result.stdout}\n推送错误:\n{push_result.stderr}"
        
        logger.info(f"命令执行成功: {result.stdout[:100]}...")
        return result.stdout
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Git操作失败: {e.stderr}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"发生错误: {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
def check_collection_commits(
    project_pattern: str = typer.Option("collection", help="项目名称匹配模式"),
    branch: str = typer.Option("master", help="要查看的分支名称")
) -> str:
    """
    查看指定模式的项目分支最近提交记录
    
    Args:
        project_pattern: 项目名称匹配模式
        branch: 分支名称
        
    Returns:
        提交记录信息
    """
    if not gitlab_connector:
        error_msg = "GitLab连接器未初始化，请检查配置"
        logger.error(error_msg)
        return error_msg
        
    try:
        # 获取所有项目
        projects = gitlab_connector.gl.projects.list(all=True)
        
        # 过滤项目
        filtered_projects = [p for p in projects if project_pattern in p.name]
        
        if not filtered_projects:
            msg = f"没有找到包含 {project_pattern} 的项目"
            logger.warning(msg)
            return msg
            
        result = []
        result.append(f"找到 {len(filtered_projects)} 个匹配的项目:\n")
        
        # 遍历每个项目
        for project in filtered_projects:
            try:
                result.append(f"\n项目: {project.name}")
                result.append(f"URL: {project.web_url}")
                
                # 获取指定分支
                try:
                    branch_info = project.branches.get(branch)
                    result.append(f"分支: {branch_info.name}")
                    
                    # 获取最近一次提交
                    commit = branch_info.commit
                    if isinstance(commit, dict):
                        result.append(f"最近提交: {commit.get('id', '未知')[:8]}")
                        result.append(f"提交信息: {commit.get('message', '未知')}")
                        result.append(f"提交时间: {format_date(commit.get('committed_date', '未知'))}")
                        result.append(f"提交者: {commit.get('author_name', '未知')}")
                    else:
                        result.append(f"最近提交: {commit.id[:8]}")
                        result.append(f"提交信息: {commit.message}")
                        result.append(f"提交时间: {format_date(commit.committed_date)}")
                        result.append(f"提交者: {commit.author_name}")
                    
                except gitlab.exceptions.GitlabGetError:
                    result.append(f"⚠️ 无法获取{branch}分支信息")
                    
            except Exception as e:
                result.append(f"处理项目 {project.name} 时出错: {str(e)}")
                
        return "\n".join(result)
        
    except Exception as e:
        error_msg = f"发生错误: {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
def list_project_branches(
    project_name: str = typer.Option(..., help="项目名称或路径"),
) -> str:
    """
    列出项目的所有分支
    
    Args:
        project_name: 项目名称或路径
        
    Returns:
        分支列表信息
    """
    if not gitlab_connector:
        error_msg = "GitLab连接器未初始化，请检查配置"
        logger.error(error_msg)
        return error_msg
        
    try:
        # 获取项目
        project = gitlab_connector.gl.projects.get(project_name)
        branches = project.branches.list()
        
        if not branches:
            msg = f"项目 {project_name} 没有任何分支"
            logger.warning(msg)
            return msg
            
        result = [f"项目 {project_name} 的分支列表:"]
        for branch in branches:
            result.append(f"\n分支: {branch.name}")
            commit = branch.commit
            result.append(f"最近提交: {commit['id'][:8]}")
            result.append(f"提交信息: {commit['message']}")
            result.append(f"提交时间: {format_date(commit['committed_date'])}")
            result.append(f"提交者: {commit['author_name']}")
            
        return "\n".join(result)
        
    except gitlab.exceptions.GitlabGetError as e:
        error_msg = f"获取项目失败: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"发生错误: {str(e)}"
        logger.error(error_msg)
        return error_msg

@app.command()
def create_merge_request(
    project_path: str = typer.Argument(..., help="项目路径"),
    source_branch: str = typer.Argument(..., help="源分支"),
    target_branch: str = typer.Option("master", help="目标分支"),
    title: str = typer.Argument(..., help="合并请求标题"),
    description: str = typer.Option("", help="合并请求描述")
) -> str:
    """
    创建合并请求
    
    Args:
        project_path: 项目路径
        source_branch: 源分支
        target_branch: 目标分支
        title: 合并请求标题
        description: 合并请求描述
        
    Returns:
        合并请求URL或错误信息
    """
    try:
        connector = gitlab_connector
        mr_url = connector.create_merge_request(
            project_path=project_path,
            source_branch=source_branch,
            target_branch=target_branch,
            title=title,
            description=description
        )
        if mr_url:
            return f"合并请求创建成功: {mr_url}"
        else:
            return "创建合并请求失败"
    except Exception as e:
        return f"发生错误: {str(e)}"

@app.command()
def list_projects() -> str:
    """
    列出所有GitLab项目
    
    Returns:
        项目列表信息
    """
    try:
        connector = gitlab_connector
        projects = connector.gl.projects.list(all=True)
        
        if not projects:
            return "没有找到任何项目"
            
        result = []
        result.append(f"找到 {len(projects)} 个项目:\n")
        
        for project in projects:
            result.append(f"\n项目: {project.name}")
            result.append(f"路径: {project.path_with_namespace}")
            result.append(f"描述: {project.description or '无'}")
            result.append(f"可见性: {project.visibility}")
            result.append(f"URL: {project.web_url}")
            
        return "\n".join(result)
        
    except Exception as e:
        return f"发生错误: {str(e)}"

@app.command(name="mcp-command")
def mcp_command(
    command: str = typer.Argument(..., help="自然语言命令")
) -> str:
    """
    处理Cursor MCP的自然语言命令
    
    Args:
        command: 用户输入的自然语言命令
        
    Returns:
        命令执行结果
    """
    try:
        # 处理代码改动相关的命令
        if any(keyword in command.lower() for keyword in ["总结改动", "查看修改", "代码改动"]):
            return summarize_changes()
        elif any(keyword in command.lower() for keyword in ["生成注释", "生成comment"]):
            return generate_comment()
        elif any(keyword in command.lower() for keyword in ["提交代码", "提交修改"]):
            return commit_and_push()
            
        # 处理项目相关的命令
        elif any(keyword in command.lower() for keyword in ["项目", "仓库", "代码库"]):
            if any(keyword in command.lower() for keyword in ["列表", "所有", "我的"]):
                return list_projects()
            elif any(keyword in command.lower() for keyword in ["分支", "分支列表"]):
                project_name = extract_project_name(command)
                if project_name:
                    return list_project_branches(project_name)
                else:
                    return "请指定要查看的项目名称"
            elif any(keyword in command.lower() for keyword in ["提交", "最近提交"]):
                return check_collection_commits()
                
        # 处理Git操作相关的命令
        elif any(keyword in command.lower() for keyword in ["更新", "拉取", "同步"]):
            return git_operation("/test/repo", "更新代码")
        elif any(keyword in command.lower() for keyword in ["推送", "上传"]):
            return git_operation("/test/repo", "推送代码")
        elif any(keyword in command.lower() for keyword in ["创建分支", "新建分支"]):
            branch_name = extract_branch_name(command)
            if branch_name:
                return git_operation("/test/repo", f"创建分支 {branch_name}")
            else:
                return "请指定要创建的分支名称"
        elif any(keyword in command.lower() for keyword in ["切换分支", "切换到"]):
            branch_name = extract_branch_name(command)
            if branch_name:
                return git_operation("/test/repo", f"切换分支 {branch_name}")
            else:
                return "请指定要切换的分支名称"
            
        return "抱歉，我暂时无法理解您的命令。您可以尝试以下操作：\n" + \
               "- 总结代码改动\n" + \
               "- 生成提交注释\n" + \
               "- 提交代码\n" + \
               "- 查看我的项目\n" + \
               "- 查看项目分支\n" + \
               "- 查看最近提交\n" + \
               "- 更新代码\n" + \
               "- 推送代码\n" + \
               "- 创建新分支\n" + \
               "- 切换到指定分支"
               
    except Exception as e:
        return f"发生错误: {str(e)}"

def summarize_changes() -> str:
    """
    总结代码改动
    
    Returns:
        改动总结
    """
    try:
        # 获取git status输出
        result = subprocess.run(
            ["git", "status", "-s"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if not result.stdout.strip():
            return "没有检测到任何改动"
            
        # 分析改动
        changes = result.stdout.split("\n")
        summary = []
        summary.append("检测到以下改动：\n")
        
        for change in changes:
            if not change.strip():
                continue
            status, file = change.split()
            if status == "M":
                summary.append(f"📝 修改: {file}")
            elif status == "A":
                summary.append(f"➕ 新增: {file}")
            elif status == "D":
                summary.append(f"❌ 删除: {file}")
            elif status == "??":
                summary.append(f"❓ 未跟踪: {file}")
                
        return "\n".join(summary)
        
    except Exception as e:
        return f"总结改动时发生错误: {str(e)}"

def generate_comment() -> str:
    """
    生成提交注释
    
    Returns:
        生成的注释
    """
    try:
        # 获取git diff输出
        result = subprocess.run(
            ["git", "diff"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if not result.stdout.strip():
            return "没有检测到任何改动，无法生成注释"
            
        # 这里可以添加更复杂的注释生成逻辑
        # 目前只是简单生成一个注释
        comment = """
        [MCP] 自动提交
        
        主要改动：
        1. 修复了一些bug
        2. 优化了代码结构
        3. 添加了新功能
        
        详细改动请查看代码diff
        """
        
        return comment.strip()
        
    except Exception as e:
        return f"生成注释时发生错误: {str(e)}"

def commit_and_push() -> str:
    """
    提交代码并推送到远程
    
    Returns:
        执行结果
    """
    try:
        # 生成注释
        comment = generate_comment()
        
        # 提交代码
        subprocess.run(
            ["git", "add", "."],
            check=True
        )
        
        subprocess.run(
            ["git", "commit", "-m", comment],
            check=True
        )
        
        # 推送到远程
        subprocess.run(
            ["git", "push"],
            check=True
        )
        
        return "代码已成功提交并推送到远程仓库"
        
    except Exception as e:
        return f"提交代码时发生错误: {str(e)}"

def extract_project_name(command: str) -> Optional[str]:
    """
    从自然语言命令中提取项目名称
    
    Args:
        command: 自然语言命令
        
    Returns:
        项目名称或None
    """
    # 这里可以添加更复杂的项目名称提取逻辑
    # 目前只是简单返回一个示例项目名称
    return "test/repo"

def extract_branch_name(command: str) -> Optional[str]:
    """
    从自然语言命令中提取分支名称
    
    Args:
        command: 自然语言命令
        
    Returns:
        分支名称或None
    """
    # 这里可以添加更复杂的分支名称提取逻辑
    # 目前只是简单返回一个示例分支名称
    return "feature/new-branch"

def main():
    """
    MCP插件入口点
    """
    try:
        return mcp.run()
    except Exception as e:
        logger.error(f"MCP服务运行错误: {str(e)}")
        return str(e)

if __name__ == "__main__":
    app() 