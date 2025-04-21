"""
GitLab MCP服务测试用例
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from src.gitlab_mcp.connector import GitLabConnector
from src.gitlab_mcp.server import git_operation, create_merge_request, get_gitlab_connector, set_gitlab_connector
import subprocess

class TestGitLabMCP(unittest.TestCase):
    """GitLab MCP服务测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 设置测试环境变量
        os.environ["GITLAB_API_BASE"] = "http://test-gitlab.com"
        os.environ["GITLAB_ACCESS_TOKEN"] = "test-token"
        os.environ["ALLOWED_PATHS"] = "/test/repo"
        
        # 设置测试模式的GitLab连接器
        set_gitlab_connector(GitLabConnector(test_mode=True))
        
    def tearDown(self):
        """测试后的清理工作"""
        # 清理GitLab连接器
        set_gitlab_connector(None)
        
    @patch('subprocess.run')
    def test_git_pull(self, mock_run):
        """测试git pull操作"""
        # 设置模拟返回值
        mock_run.return_value = MagicMock(
            stdout="Already up to date",
            stderr="",
            returncode=0
        )
        
        # 执行测试
        result = git_operation("/test/repo", "更新代码")
        
        # 验证结果
        self.assertIn("up to date", result)
        mock_run.assert_called_once()
        
    def test_create_merge_request(self):
        """测试创建合并请求"""
        # 执行测试
        result = create_merge_request(
            project_path="test/project",
            source_branch="feature/test",
            target_branch="main",
            title="Test MR"
        )
        
        # 验证结果
        self.assertIn("合并请求创建成功", result)
        self.assertIn("http://test-gitlab.com/merge/1", result)
        
    def test_invalid_path(self):
        """测试无效路径"""
        result = git_operation("/invalid/path", "更新代码")
        self.assertIn("不在允许列表中", result)
        
    @patch('subprocess.run')
    def test_git_error(self, mock_run):
        """测试Git操作错误"""
        # 设置模拟错误
        mock_run.side_effect = subprocess.CalledProcessError(1, "git", stderr="Error message")
        
        # 执行测试
        result = git_operation("/test/repo", "更新代码")
        
        # 验证结果
        self.assertIn("操作失败", result)
        
if __name__ == '__main__':
    unittest.main() 