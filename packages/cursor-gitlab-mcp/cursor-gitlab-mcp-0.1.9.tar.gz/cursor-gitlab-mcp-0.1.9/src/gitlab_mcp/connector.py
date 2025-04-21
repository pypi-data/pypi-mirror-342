"""
GitLab连接模块 - 提供GitLab API的封装和认证管理
"""

from typing import Optional, Dict, Any, List
import os
import logging
from pathlib import Path
from urllib.parse import urljoin
from python_gitlab import Gitlab
from python_gitlab.exceptions import GitlabError, GitlabAuthenticationError
from datetime import datetime, timedelta

# 配置日志目录
log_dir = os.path.join(str(Path.home()), '.local', 'share', 'gitlab_mcp')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'gitlab_mcp.log')

# 配置日志
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "DEBUG"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GitLabConnector:
    """GitLab连接器类，封装GitLab API操作"""
    
    def __init__(self):
        """初始化GitLab连接器"""
        self.gl = None
        self._initialize_gitlab()
        
    def _initialize_gitlab(self):
        """初始化GitLab连接"""
        try:
            # 获取环境变量
            api_base = os.getenv('GITLAB_API_BASE')
            access_token = os.getenv('GITLAB_ACCESS_TOKEN')
            
            if not api_base or not access_token:
                logger.error("缺少必要的环境变量: GITLAB_API_BASE 或 GITLAB_ACCESS_TOKEN")
                raise ValueError("缺少必要的环境变量")
            
            logger.info(f"正在连接到GitLab服务器: {api_base}")
            
            # 初始化GitLab客户端
            self.gl = Gitlab(
                url=api_base,
                private_token=access_token,
                ssl_verify=False
            )
            
            # 测试连接
            self.gl.auth()
            logger.info("GitLab连接成功")
            
        except Exception as e:
            logger.error(f"GitLab连接失败: {str(e)}")
            raise
            
    def test_connection(self) -> bool:
        """
        测试GitLab连接是否正常
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.gl.auth()
            logger.info("GitLab连接测试成功")
            return True
        except Exception as e:
            logger.error(f"GitLab连接测试失败: {str(e)}")
            return False
            
    def get_project(self, project_path: str) -> Optional[Dict[str, Any]]:
        """
        根据项目路径获取项目信息
        
        Args:
            project_path: 项目路径，格式为"namespace/project"
            
        Returns:
            项目信息字典，如果获取失败则返回None
        """
        try:
            project = self.gl.projects.get(project_path)
            logger.info(f"成功获取项目: {project_path}")
            return project.attributes
        except GitlabError as e:
            logger.error(f"获取项目失败: {str(e)}")
            return None
            
    def create_merge_request(self, project_path: str, source_branch: str, 
                           target_branch: str, title: str, description: str = "") -> Optional[str]:
        """
        创建合并请求
        
        Args:
            project_path: 项目路径
            source_branch: 源分支
            target_branch: 目标分支
            title: 合并请求标题
            description: 合并请求描述
            
        Returns:
            合并请求的URL，如果创建失败则返回None
        """
        try:
            project = self.gl.projects.get(project_path)
            mr = project.mergerequests.create({
                'source_branch': source_branch,
                'target_branch': target_branch,
                'title': title,
                'description': description
            })
            logger.info(f"成功创建合并请求: {mr.web_url}")
            return mr.web_url
        except GitlabError as e:
            logger.error(f"创建合并请求失败: {str(e)}")
            return None
            
    def get_branches(self, project_path: str) -> Optional[list]:
        """
        获取项目分支列表
        
        Args:
            project_path: 项目路径
            
        Returns:
            分支列表，如果获取失败则返回None
        """
        try:
            project = self.gl.projects.get(project_path)
            branches = [branch.name for branch in project.branches.list()]
            logger.info(f"成功获取分支列表: {project_path}")
            return branches
        except GitlabError as e:
            logger.error(f"获取分支列表失败: {str(e)}")
            return None

    def list_projects(self) -> List[Dict[str, Any]]:
        """获取项目列表"""
        try:
            logger.info("开始获取项目列表")
            projects = self.gl.projects.list(all=True)
            logger.info(f"成功获取到 {len(projects)} 个项目")
            return [{
                'id': p.id,
                'name': p.name,
                'path': p.path,
                'description': p.description,
                'web_url': p.web_url
            } for p in projects]
        except Exception as e:
            logger.error(f"获取项目列表失败: {str(e)}")
            raise
            
    def list_project_branches(self, project_path: str) -> List[Dict[str, Any]]:
        """获取项目分支列表"""
        try:
            logger.info(f"开始获取项目 {project_path} 的分支列表")
            project = self.gl.projects.get(project_path)
            branches = project.branches.list()
            logger.info(f"成功获取到 {len(branches)} 个分支")
            return [{
                'name': b.name,
                'commit': b.commit['id'],
                'message': b.commit['message'],
                'author': b.commit['author_name'],
                'date': b.commit['committed_date']
            } for b in branches]
        except Exception as e:
            logger.error(f"获取分支列表失败: {str(e)}")
            raise
            
    def check_collection_commits(self, days: int = 7) -> List[Dict[str, Any]]:
        """获取最近提交"""
        try:
            logger.info(f"开始获取最近 {days} 天的提交记录")
            since = (datetime.now() - timedelta(days=days)).isoformat()
            commits = []
            
            # 获取所有项目
            projects = self.gl.projects.list(all=True)
            logger.info(f"开始扫描 {len(projects)} 个项目")
            
            for project in projects:
                try:
                    project_commits = project.commits.list(since=since)
                    for commit in project_commits:
                        commits.append({
                            'project': project.name,
                            'id': commit.id,
                            'title': commit.title,
                            'author': commit.author_name,
                            'date': commit.committed_date,
                            'message': commit.message
                        })
                except Exception as e:
                    logger.warning(f"获取项目 {project.name} 的提交记录失败: {str(e)}")
                    continue
                    
            logger.info(f"成功获取到 {len(commits)} 条提交记录")
            return commits
        except Exception as e:
            logger.error(f"获取提交记录失败: {str(e)}")
            raise 