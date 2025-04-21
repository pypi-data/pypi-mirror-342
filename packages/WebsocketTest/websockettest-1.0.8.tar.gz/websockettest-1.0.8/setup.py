from setuptools import find_packages, setup
from setuptools.command.sdist import sdist
from setuptools.command.bdist_wheel import bdist_wheel

class CustomSdist(sdist):
    def initialize_options(self):
        super().initialize_options()
        self.dist_dir = "setup_temp/dist"  # 自定义sdist路径

class CustomBdistWheel(bdist_wheel):
    def initialize_options(self):
        super().initialize_options()
        self.dist_dir = "setup_temp/dist"  # 自定义wheel路径

setup(
    cmdclass={
        'sdist': CustomSdist,
        'bdist_wheel': CustomBdistWheel
    },
    name="WebsocketTest",
    version="1.0.8",
    author='chencheng',
    python_requires=">=3.10",
    packages=find_packages(exclude=["WebsocketTest.allure_report", "WebsocketTest.logs", "WebsocketTest.allure_results",  "WebsocketTest.config", "WebsocketTest.data","WebsocketTest.testcase"]),
    description="websocket api autotest",
    install_requires = [
        "allure_python_commons==2.13.5",
        "numpy==2.2.4",
        "pandas==2.2.3",
        "pytest==8.2.2",
        "PyYAML==6.0.2",
        "websockets==12.0"
    ],
    entry_points={
        'console_scripts': [
            "ws=WebsocketTest.cli:main"
        ]
    }
)
# import shutil

# # 清理 .egg-info 文件夹
# shutil.rmtree('WebsocketTest.egg-info', ignore_errors=True)