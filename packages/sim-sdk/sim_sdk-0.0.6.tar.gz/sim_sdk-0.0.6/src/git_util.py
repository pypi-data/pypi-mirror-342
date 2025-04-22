import logging
import os
import shutil
import subprocess
import sys
from urllib.parse import quote
from typing import List
import json
from pathlib import Path
from util import nacos_client
import data_deal_util
import inspect

# 通过 get_config() 函数获取配置（懒加载）
current_config = nacos_client.get_config()

# 添加当前目录到 Python 路径中
sys.path.append(os.path.dirname(__file__))

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GitFileDownloader:
    def __init__(self, repo_url, local_path, username=None, password=None):
        self.repo_url = repo_url
        self.local_path = local_path
        self.username = username
        self.password = password

    def checkout_commit(self, commit_hash, repo_url_with_credentials):
        """
        拉取所有提交并切换到指定的提交哈希.

        :param commit_hash: 提交哈希
        """
        # 初始化一个空的本地仓库
        subprocess.run(
            ['git', 'init', self.local_path],
            check=True
        )

        # 添加远程仓库
        subprocess.run(
            ['git', '-C', self.local_path, 'remote', 'add', 'origin', repo_url_with_credentials],
            check=True
        )

        # 使用 fetch 拉取所有提交记录（可选使用 --depth 限制数量）
        subprocess.run(
            ['git', '-C', self.local_path, 'fetch', '--depth', '10'],
            check=True
        )

        # 切换到指定的提交哈希
        subprocess.run(
            ['git', '-C', self.local_path, 'checkout', commit_hash],
            check=True
        )

        logging.info(f"成功切换到提交 {commit_hash}")

    def fetch_specific_branch(self, branch_name, repo_url_with_credentials):
        """
        拉取指定分支的更新.

        :param branch_name: 分支名称
        """
        subprocess.run(
            ['git', 'clone', '--depth', '10', '--branch', branch_name,
             repo_url_with_credentials, self.local_path],
            check=True
        )

        logging.info(f"成功拉取分支 {branch_name} 的更新")

    def clone_and_checkout(self, branch_or_commit):
        """
        使用浅克隆克隆仓库并切换到指定分支或 commit.

        :param branch_or_commit: 分支名或提交哈希
        """
        # 如果有用户名和密码，构建带凭据的仓库 URL
        encoded_username = quote(self.username) if self.username else ''
        encoded_password = quote(self.password) if self.password else ''
        auth = f"{encoded_username}:{encoded_password}@" if encoded_username and encoded_password else ""
        repo_url_with_credentials = self.repo_url.replace("https://", f"https://{auth}")

        # 尝试使用 --branch 克隆，判断是否为分支名
        try:
            self.fetch_specific_branch(branch_or_commit, repo_url_with_credentials)
        except subprocess.CalledProcessError:
            logging.exception(f"克隆分支 {branch_or_commit} 时出错")
            # 如果克隆分支失败，删除已创建的目录
            if os.path.exists(self.local_path):
                shutil.rmtree(self.local_path)
            # 如果克隆分支失败，执行常规克隆并尝试 checkout 到提交哈希
            try:
                self.checkout_commit(branch_or_commit, repo_url_with_credentials)
                logging.error(f"成功切换到提交哈希 {branch_or_commit}")
            except subprocess.CalledProcessError as e:
                logging.error(f"切换到指定的commit 时出错: {e}")
                raise e

    def copy_file(self, file_path_in_repo: list, output_local_path: list):
        """
        复制仓库中的指定文件到本地.

        :param file_path_in_repo: 仓库中的文件路径
        :param output_local_path: 本地输出路径
        """
        # 确保仓库已经存在
        if not os.path.exists(self.local_path):
            raise FileNotFoundError(
                f"Local repository path '{self.local_path}' does not exist. Clone the repository first.")

        for index, file_path in enumerate(file_path_in_repo):
            # 确保输出文件的目录存在
            output_dir = os.path.dirname(output_local_path[index])
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 复制文件
            full_file_path = os.path.join(self.local_path, file_path_in_repo[index])
            shutil.copy(full_file_path, output_local_path[index])
            logging.info(f"成功复制文件到 {output_local_path[index]}")


def get_file(file_path_in_repo: List[str], output_local_path: List[str], branch_or_commit, repo_url=None, local_path=None):
    """
    拉取 Git 仓库中的指定文件并保存到本地.

    :param file_path_in_repo: 仓库内的文件路径
    :param output_local_path: 本地保存路径
    :param repo_url: 仓库地址
    :param local_path: 本地路径
    :param branch_or_commit: 分支名或提交哈希
    """
    try:
        # 从配置中获取默认参数值，如果未传递这些参数
        if repo_url is None:
            repo_url = current_config.get("git").get("repo_url")
        if local_path is None:
            local_path = current_config.get("git").get("local_path")

        if not repo_url or not local_path or not branch_or_commit:
            raise ValueError("repo_url, local_path 或 branch_or_commit 参数不能为空")\

        if isinstance(file_path_in_repo, str):
            file_path_in_repo = [file_path_in_repo]

        if isinstance(output_local_path, str):
            output_local_path = [output_local_path]

        downloader = GitFileDownloader(repo_url, local_path, current_config.get("git").get("username"), current_config.get("git").get("password"))
        downloader.clone_and_checkout(branch_or_commit)  # 克隆并切换到特定分支或 commit
        downloader.copy_file(file_path_in_repo, output_local_path)  # 下载文件
        return True
    except Exception as e:
        logging.exception(f"文件下载失败")
        return False


def copy_file(file_path_in_repo: List[str], output_local_path: List[str], branch_or_commit, repo_url=None, local_path=None):
    """
    拷贝已经在本地Git仓库中的指定文件到指定目录，不会真正从远程仓库拉取文件.

    :param file_path_in_repo: 仓库内的文件路径
    :param output_local_path: 本地保存路径
    :param repo_url: 仓库地址
    :param local_path: 本地路径
    :param branch_or_commit: 分支名或提交哈希
    """
    try:
        # 从配置中获取默认参数值，如果未传递这些参数
        if repo_url is None:
            repo_url = current_config.get("git").get("repo_url")
        if local_path is None:
            local_path = current_config.get("git").get("local_path")

        if not repo_url or not local_path or not branch_or_commit:
            raise ValueError("repo_url, local_path 或 branch_or_commit 参数不能为空")\

        if isinstance(file_path_in_repo, str):
            file_path_in_repo = [file_path_in_repo]

        if isinstance(output_local_path, str):
            output_local_path = [output_local_path]

        downloader = GitFileDownloader(repo_url, local_path, current_config.get("git").get("username"), current_config.get("git").get("password"))
        # 直接拷贝
        downloader.copy_file(file_path_in_repo, output_local_path)
        return True
    except Exception as e:
        logging.exception(f"文件下载失败")
        return False


def parse_operator_info_by_json(json_file_path, bc_name: str):
    """
        解析算子json文件，获取算子脚本及对应的配置信息

        @param json_local_path: 算子json文件本地路径
    """
    # 删除上一次的git代码
    data_deal_util.change_permissions_and_delete(current_config.get("git", {}).get("local_path"))

    json_local_file = download_git_file(bc_name, [json_file_path])
    # 解析算子json文件
    try:
        with open(json_local_file[0], 'r', encoding='utf-8') as file:
            metric_json = json.loads(file.read())
    except Exception as err:
        logging.error(f'{json_local_file}  json解析失败：' + str(err))

    # 获取需要执行的算子脚本文件列表
    enabled_metric_list = metric_json['enabled_metric_list']
    # 获取每个算子脚本对应的配置信息
    metric_config_json = metric_json['metric_config']

    # 算子脚本文件下载到本地的目录
    script_local_path_list = download_git_file(bc_name, enabled_metric_list, need_download=False)

    return script_local_path_list, json_local_file, metric_config_json, metric_json


def parse_debug_operator_info_by_json(json_file_path, bc_name: str):
    """
        解析算子json文件，获取算子脚本及对应的配置信息，debug模式直接使用本地代码文件
        @param json_local_path: 算子json文件本地路径
    """
    # 删除上一次的git代码
    data_deal_util.change_permissions_and_delete(current_config.get("git", {}).get("local_path"))
    operator_src = get_src_root()  # os.getenv('OPERATOR_SRC')
    # 解析算子json文件
    try:
        with open(f"{operator_src}/" + json_file_path, 'r', encoding='utf-8') as file:
            metric_json = json.loads(file.read())
    except Exception as err:
        logging.error(f'{json_file_path}  json解析失败：' + str(err))
        raise ValueError(f'文件 {json_file_path} json解析失败【请确保文件存在，路径正确】：' + str(err))

    # 获取需要执行的算子脚本文件列表
    enabled_metric_list = metric_json['enabled_metric_list']
    # 获取每个算子脚本对应的配置信息
    metric_config_json = metric_json['metric_config']

    # 本地的目录算子脚本文件
    script_local_path_list = []
    for operator in enabled_metric_list:
        script_local_path_list.append(f"{operator_src}/" + operator)
    logging.info(f"script_local_path_list: {script_local_path_list}")
    return script_local_path_list, metric_config_json


def get_src_root():
    stack = inspect.stack()
    for frame_info in stack:
        caller_file = Path(frame_info.filename).resolve()
        # 跳过 site-packages 的路径
        if 'site-packages' not in str(caller_file):
            parts = caller_file.parts
            if 'src' in parts:
                src_index = parts.index('src')
                src_path = Path(*parts[:src_index + 1])
                return src_path
    return None

def download_git_file(bc_name, file_path_lis: list, need_download=True):
    """
        下载git项目文件：算子脚本文件、配置文件等
        @param file_path_lis: 算子脚本文件列表
        @param need_download: 是否需要下载，如果为False，则直接从本地复制文件
        @param bc_name: 算子仓库分支或commit id
    """

    logging.info(f"start download git file: {file_path_lis}")

    # 算子脚本文件下载并考本指定算子文件到指定目录
    local_path_prefix = current_config.get('containerPath')
    # 算子脚本文件下载到本地的路径
    script_local_file_path_list = [local_path_prefix + path for path in file_path_lis]

    # 算子脚本在git项目中的完整路径 src/eval/xxx.py
    src_op_file_path_list = ["src/" + path for path in file_path_lis]

    if need_download:
        git_result = get_file(src_op_file_path_list, script_local_file_path_list, bc_name)
    else:
        git_result = copy_file(src_op_file_path_list, script_local_file_path_list, bc_name)

    if not git_result:
        raise Exception("算子下载失败 op_file_name:{}".format(src_op_file_path_list))
    logging.info("成功下载算子: %s" % src_op_file_path_list)
    logging.info("算子保存在: %s" % script_local_file_path_list)
    return script_local_file_path_list

if __name__ == "__main__":
    get_file("test_operator.py", "/home/datacenter/operator/test_operator.py", "test_branch")
    # get_file("test_operator.py", "/home/datacenter/operator/test_operator.py", "0d95b6a7")