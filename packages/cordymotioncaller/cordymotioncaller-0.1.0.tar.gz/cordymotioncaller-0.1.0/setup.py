from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        # 安装后自动验证
        import cordymotioncaller.CordyMotionCaller
        caller = cordymotioncaller.MotionCaller()
        caller.run_check()

# 获取TcpClient二进制文件的安装路径
def get_bin_path():
    return os.path.join(os.path.dirname(__file__), "cordymotioncaller", "bin")

setup(
    cmdclass={
        "install": PostInstallCommand,
    },
    name="cordymotioncaller",          # PyPI包名（需唯一）
    version="0.1.0",               # 版本号
    packages=find_packages(),      # 自动发现包
    include_package_data=True,     # 包含非Python文件
    package_data={
        "cordymotioncaller": ["bin/*"],  # 包含bin目录下的所有文件
    },
    install_requires=[],           # 依赖项（如无需则留空）
    entry_points={
        "console_scripts": [       # 可选的命令行工具
            "cordymotioncaller-cli = cordymotioncaller.MotionCaller:main",
        ],
    },
    description="Python wrapper for MotionCaller",  # 包描述
    long_description=open("README.md").read(),    # 长描述（通常用README）
    long_description_content_type="text/markdown",
)