
from WebsocketTest.run_tests import TestRunner


def configure_parser(parser):
    """配置子命令参数"""
    parser.add_argument("--env", required=True, help="Test environment")
    parser.add_argument("--app", required=True, help="Application ID")
    parser.add_argument("--service", required=True, help="Service name")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--port", type=int, default=8883, help="Allure report port")
    parser.add_argument("--report-dir", default="allure_report", help="Allure report directory")
    parser.add_argument("--testcase", required=False, help='Specify the test case to run (e.g., "testcase/test_all.py::TestAqua::test_api[case_suite0]"')

def execute(args):
    """执行test"""
    test_runner = TestRunner(args)
    exit(test_runner.run())
# 注册到主CLI
func = execute