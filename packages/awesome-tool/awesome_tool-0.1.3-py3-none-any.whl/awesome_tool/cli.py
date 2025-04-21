"""
Command-line interface for awesome_tool.
"""

import argparse
import sys
from awesome_tool import __version__

import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
def get_desktop_files():
    """获取桌面上的文件列表"""
    return os.listdir(os.path.expanduser("~/Desktop"))
@mcp.tool()
def get_desktop_files_based_on_path(directory: str = os.path.expanduser("~/Desktop")):
    """根据指定的目录获取所有的文件列表"""
    return os.listdir(directory)

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
