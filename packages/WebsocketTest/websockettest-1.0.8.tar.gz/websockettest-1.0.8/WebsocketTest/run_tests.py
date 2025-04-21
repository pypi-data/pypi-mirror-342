import subprocess
import argparse
import shutil
import time
import webbrowser
from urllib.request import urlopen
from urllib.error import URLError
from pathlib import Path
from WebsocketTest.common.logger import logger

class AllureManager:
    def __init__(self, port: int = 8883):
        self.port = port
        self.allure_path = shutil.which("allure")
        if not self.allure_path:
            raise RuntimeError("Allure command line tool not found in PATH")

    def is_server_running(self) -> bool:
        """检查Allure服务是否已在运行"""
        try:
            with urlopen(f"http://localhost:{self.port}") as response:
                return response.status == 200
        except URLError:
            return False

    def start_server(self, report_dir: str) -> bool:
        """启动Allure服务"""
        try:
            cmd = [self.allure_path, "open", report_dir, "-p", str(self.port)]
            # logger.info(f"start_server Executing: {' '.join(cmd)}")
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            time.sleep(3)  # 等待服务启动
            return True
        except Exception as e:
            logger.error(f"Failed to start Allure server: {e}")
            return False

    def refresh_browser_tab(self) -> bool:
        """尝试刷新已打开的Allure标签页"""
        url = f"http://localhost:{self.port}"
        
        # 方法1: 使用JavaScript刷新（需要浏览器支持）
        try:
            webbrowser.open_new_tab("javascript:location.reload(true);")
            return True
        except Exception as e:
            logger.warning(f"JavaScript refresh failed: {e}")
        
        # 方法2: 使用webbrowser直接打开（会聚焦到已有标签页）
        try:
            browser = webbrowser.get() # 获取系统默认浏览器控制器
            if hasattr(browser, 'open_new_tab'):
                browser.open_new_tab(url)  # 大多数浏览器会聚焦到已有标签页
                return True
        except Exception as e:
            logger.error(f"Browser refresh failed: {e}")
        
        return False

class TestRunner:
    def __init__(self, args):
        """直接存储args对象"""
        self.args = args
        self.allure_manager = AllureManager(self.args.port)
        self.allure_results = str(Path.cwd().joinpath("allure_results"))

    def run_pytest_tests(self) -> bool:
        """执行pytest测试"""  
        # 构建基础命令列表
        cmd = [
            "pytest",
            "-m", self.args.service.split('_')[0],
            "--env", self.args.env,
            "--app", self.args.app,
            "--service", self.args.service,
            "--project", self.args.project,
            "--alluredir", self.allure_results
        ]
           # 添加可选测试路径（如果存在）
        if hasattr(self.args, 'testcase') and self.args.testcase:
            cmd.insert(1, self.args.testcase)
        print(f"run_pytest_tests Executing: {' '.join(cmd)}")
        try:
            # logger.info(f"run_pytest_tests Executing: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, timeout=3600)
        except subprocess.CalledProcessError as e:
            logger.error(f"Tests failed with exit code {e.returncode}")
        except subprocess.TimeoutExpired:
            logger.error("Test execution timed out after 1 hour")

    def generate_allure_report(self) -> bool:
        """生成Allure报告"""
        try:
            cmd = [self.allure_manager.allure_path, "generate", self.allure_results, "-o", self.args.report_dir, "--clean"]
            subprocess.run(
                cmd,
                check=True,
                timeout=300
            )
            # logger.info(f"generate_allure_report Executing: {' '.join(cmd)}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Report generation failed: {e}")
    def _handle_allure_report(self) -> bool:
        """Handle Allure report serving and browser opening."""
        if  self.allure_manager.is_server_running():
            logger.info("Refreshing existing Allure report tab...")
            if not self.allure_manager.refresh_browser_tab():
                logger.info("Opening new report...")
                webbrowser.open(f"http://localhost:{self.args.port}")
        else:
            logger.info("Starting new Allure server...")
            if self.allure_manager.start_server(self.args.report_dir):
                webbrowser.open(f"http://localhost:{self.args.port}")
    def run(self):
        # 1. 运行测试
        self.run_pytest_tests()

        # 2. 生成报告数据
        self.generate_allure_report()

        # 3. 启动Allure服务
        self._handle_allure_report()
        logger.info(f"http://localhost:{self.args.port}")
        return 0

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Run tests with Allure reporting")
        parser.add_argument("--env", required=True, help="Test environment")
        parser.add_argument("--app", required=True, help="Application ID")
        parser.add_argument("--service", required=True, help="Service name")
        parser.add_argument("--project", required=True, help="Project name")
        parser.add_argument("--port", type=int, default=8883, help="Allure report port")
        parser.add_argument("--report-dir", default="allure_report", help="Allure report directory")
        parser.add_argument("--testcase", required=False, help='Specify the test case to run (e.g., "testcase/test_all.py::TestAqua::test_api[case_suite0]"')
        args = parser.parse_args()
        test_runner = TestRunner(args)
        exit(test_runner.run())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        exit(1)  