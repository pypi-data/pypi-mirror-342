import pytest
import yaml
from pathlib import Path

# 设置环境信息的 fixture
@pytest.fixture(scope="session")
def setup_env(request):
    # 获取命令行参数
    service = request.config.getoption("service")
    project = request.config.getoption("project")
    env = request.config.getoption("env")
    app_id = request.config.getoption("app")
     # 获取当前工作目录，并解析为绝对路径
    current_working_directory = Path.cwd().resolve()
    config_dir = current_working_directory.joinpath('config', project)
    
    # Load base configuration
    with open(config_dir.joinpath(f'{env}.yml')) as base_file:
        config = yaml.safe_load(base_file)
    
    # Load environment-specific configuration and merge into the base config
    with open(config_dir.joinpath(service, f'{env}.yml')) as env_file:
        env_config = yaml.safe_load(env_file)
    # 合并配置
    environments = config.get('environments', {})
    environments.update(env_config.get('environments', {}))
    # 添加运行时参数
    environments.update({'appId': app_id,
            'env_name': env,
            'service': service,
            'project': project})
    return environments

# 添加命令行选项
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="uat",
        help="Environment to use (default: uat)"
    )
    parser.addoption(
        "--app",
        action="store",
        default="0f0826ab",
        help="App to use (default: 0f0826ab)"
    )
    parser.addoption(
        "--service",
        action="store",
        default="0f0826ab",
        help="Service to use (default: aqua)"
    )
    parser.addoption(
        "--project",
        action="store",
        default="vwa",
        help="Project name is required"
    )




