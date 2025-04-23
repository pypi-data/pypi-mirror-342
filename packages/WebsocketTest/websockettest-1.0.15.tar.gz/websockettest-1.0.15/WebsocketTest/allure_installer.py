import os
import sys
import zipfile
import subprocess
import winreg
from pathlib import Path

# 配置参数
ALLURE_VERSION = "2.30.0"
PACKAGE_NAME = "WebsocketTest"  # 您的包名
LOCAL_ZIP_RELATIVE_PATH = os.path.join("libs", f"allure-{ALLURE_VERSION}.zip")  # 包内相对路径
INSTALL_DIR = os.path.expanduser("~/.allure")  # 安装到用户目录
ALLURE_BIN_DIR = os.path.join(INSTALL_DIR, f"allure-{ALLURE_VERSION}", "bin")

def is_allure_installed():
    """检查Allure是否在PATH中且可执行"""
    try:
        # 同时检查版本避免找到无效安装
        result = subprocess.run(["allure", "--version"], 
                              check=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)
        installed_version = result.stdout.strip()
        if ALLURE_VERSION not in installed_version:
            print(f"⚠️ 发现不匹配的Allure版本: {installed_version} (需要 {ALLURE_VERSION})")
            return False
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_local_zip_path():
    """获取ZIP文件的绝对路径（兼容开发模式和正式安装）"""
    # 尝试从包内获取
    try:
        import importlib.resources as pkg_resources
        with pkg_resources.path(PACKAGE_NAME, LOCAL_ZIP_RELATIVE_PATH) as zip_path:
            return str(zip_path)
    except:
        pass
    
    # 回退方案：从当前工作目录查找
    base_dirs = [
        os.getcwd(),
        os.path.dirname(os.path.abspath(__file__)),
        sys.prefix
    ]
    
    for base in base_dirs:
        zip_path = os.path.join(base, PACKAGE_NAME, LOCAL_ZIP_RELATIVE_PATH)
        if os.path.exists(zip_path):
            return zip_path
    
    raise FileNotFoundError(f"Allure ZIP文件未在任何位置找到: {LOCAL_ZIP_RELATIVE_PATH}")

def install_allure():
    """从本地ZIP安装Allure"""
    try:
        zip_path = get_local_zip_path()
        print(f"🔍 找到Allure ZIP文件: {zip_path}")

        # 创建安装目录
        os.makedirs(INSTALL_DIR, exist_ok=True)
        print(f"📦 解压到: {INSTALL_DIR}")

        # 解压ZIP文件（使用更安全的提取方法）
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                # 防止Zip Slip攻击
                safe_path = os.path.join(INSTALL_DIR, *file.split('/'))
                if file.endswith('/'):
                    os.makedirs(safe_path, exist_ok=True)
                else:
                    with open(safe_path, 'wb') as f:
                        f.write(zip_ref.read(file))

        # 设置权限（特别是Linux/macOS）
        if sys.platform != "win32":
            os.chmod(os.path.join(ALLURE_BIN_DIR, "allure"), 0o755)

        # 更新PATH
        if add_to_user_path(ALLURE_BIN_DIR):
            # 立即在当前进程生效
            os.environ["PATH"] = f"{ALLURE_BIN_DIR}{os.pathsep}{os.environ.get('PATH', '')}"
        
        return True
    except Exception as e:
        print(f"❌ 安装失败: {type(e).__name__}: {e}", file=sys.stderr)
        return False

def add_to_user_path(path):
    """添加到用户级PATH环境变量"""
    try:
        if sys.platform == "win32":
            # Windows注册表操作
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Environment",
                0,
                winreg.KEY_READ | winreg.KEY_WRITE,
            ) as key:
                current_path, _ = winreg.QueryValueEx(key, "Path")
                
                if path in current_path.split(os.pathsep):
                    return False
                
                new_path = f"{current_path}{os.pathsep}{path}" if current_path else path
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            
            # 刷新环境变量
            subprocess.run(
                'powershell -command "[Environment]::SetEnvironmentVariable(\'Path\', $env:Path + \';{}\', \'User\')"'
                .format(path),
                shell=True,
                check=True
            )
        else:
            # Linux/macOS: 修改shell配置文件
            shell_config = os.path.expanduser("~/.bashrc")
            if not os.path.exists(shell_config):
                shell_config = os.path.expanduser("~/.zshrc")
            
            with open(shell_config, "a") as f:
                f.write(f"\nexport PATH=\"$PATH:{path}\"\n")
        
        print(f"✅ 已添加PATH: {path}")
        return True
    except Exception as e:
        print(f"⚠️ 添加PATH失败: {e}\n请手动添加 {path} 到环境变量", file=sys.stderr)
        return False

def ensure_allure():
    """确保Allure已安装"""
    if is_allure_installed():
        print(f"✅ Allure {ALLURE_VERSION} 已安装")
        return True
    
    print("🔧 检测到Allure未安装，开始自动安装...")
    if install_allure():
        if not is_allure_installed():
            print("""
            \n⚠️ 安装成功但Allure仍未识别，可能是因为：
            1. 需要重启终端使PATH生效
            2. 尝试手动运行: {}
            """.format(os.path.join(ALLURE_BIN_DIR, "allure" + (".bat" if sys.platform == "win32" else ""))))
            return False
        return True
    else:
        print(f"""
        \n❌ 自动安装失败，请手动操作：
        1. 解压 {get_local_zip_path()} 到任意目录（推荐 {INSTALL_DIR}）
        2. 将解压后的bin目录添加到PATH:
           - Windows: 添加 {ALLURE_BIN_DIR} 到系统环境变量
           - Linux/macOS: 在~/.bashrc或~/.zshrc中添加:
             export PATH="$PATH:{ALLURE_BIN_DIR}"
        3. 运行 `allure --version` 验证
        """)
        return False

if __name__ == "__main__":
    if ensure_allure():
        sys.exit(0)
    sys.exit(1)