import websockets
from functools import cached_property
import asyncio
from WebsocketTest.common.utils import *
import allure
from pathlib import Path
from WebsocketTest.common.Assertion import Assert
import pytest
import traceback
class WSBaseApi:
    def __init__(self, **kwargs):
        self.request = {}
        self.response = {}
        for key, value in kwargs.items():
            setattr(self, key, value)
    async def WebSocketApi(self, extra_headers=None, chain=None):
        """
        建立WebSocket连接，根据提供的参数发送初始帧，并根据链路版本处理后续消息
        - 如果chain为v2，则调用handle_v2_chain处理消息
        - 否则，默认调用handle_v1_chain处理消息
        """
        async with websockets.connect(self.url, extra_headers=extra_headers) as ws:
            await ws.send(json.dumps(self.request, ensure_ascii=False))
            await self.handle_v2_chain(ws) if chain == "v2" else await self.handle_v1_chain(ws)
    @exception_decorator
    def run(self):
        self.request = self.build_params()
        # WebSocket连接与消息发送
        asyncio.run(self.WebSocketApi())



class BaseApiTest:
    # 定义需要子类实现的属性
    TEST_TYPE = "API自动化测试"  # 默认值，可被子类覆盖
    CASE_PATH = Path.cwd().resolve().joinpath("data/case_data.xlsx")

    @cached_property
    def API_TEST_RUNNER_CLASS(self):
        """动态加载对应的测试运行器类（自动缓存）"""
        class_prefix = self.__class__.__name__[4:]  # TestGateway -> Gateway
        module_path = f"WebsocketTest.caseScript.{class_prefix}"
        
        try:
            module = __import__(module_path, fromlist=['ApiTestRunner'])
            return module.ApiTestRunner
        except ImportError as e:
            raise ImportError(
                f"无法加载 {module_path}.ApiTestRunner，"
                "请检查模块路径和类命名是否符合规范"
            ) from e
    

    @pytest.mark.parametrize('case_suite', gen_case_suite(CASE_PATH))
    def test(self, case_suite, setup_env):
        """测试用例执行模板"""
        try:
            # 1. 合并参数
            params = merge_dicts(case_suite, setup_env)
            
            # 2. 执行测试
            runner = self.API_TEST_RUNNER_CLASS(**params)
            runner.run()
            
            # 3. 记录报告
            self._record_allure_report(runner)
            
            # 4. 执行断言
            self._execute_assertions(runner, case_suite)
            
        except Exception as e:
            self._record_error(e)
            raise
    
    def _record_allure_report(self, runner):
        """记录Allure测试报告"""
        allure.dynamic.epic(
            f"【{runner.env_name}】"
            f"【{runner.project}】"
            f"【{runner.service}】"
            f"{self.TEST_TYPE}"
        )
        allure.dynamic.story(runner.appId)
        allure.attach(runner.url, 'URL', allure.attachment_type.URI_LIST)
        allure.attach(
            f"{convert_to_json(runner.request)}", 
            'API请求', 
            allure.attachment_type.JSON
        )
        allure.attach(
            f"{convert_to_json(runner.response)}", 
            'API响应', 
            allure.attachment_type.JSON
        )
    def _execute_assertions(self, runner, case_suite):
        """执行断言逻辑"""
        with allure.step(f'【断言】{runner.number}_{runner.casename}'):
            Assert(runner.request, runner.response, case_suite)
    def _record_error(self, error):
        """记录测试错误信息"""
        allure.attach(
            str(error),
            '异常信息',
            allure.attachment_type.TEXT
        )
        allure.attach(
            traceback.format_exc(),
            '异常堆栈',
            allure.attachment_type.TEXT
        )