import sys
import argparse
import tomllib
import pathlib
from .atlisp import install_atlisp,pull,pkglist,remove,search
#from .search import search
parser = argparse.ArgumentParser(
    prog="atlisp",usage="atlisp command <pkgname/keystring>",
    description='@lisp是一个运行于 AutoCAD、中望CAD、浩辰CAD及类似兼容的CAD系统中的应用管理器。')
parser.add_argument("command",help="执行 atlisp 命令")

version = "0.1.22"
help_str = """usage: atlisp.exe command <pkgname/keystring>
@lisp是一个运行于 AutoCAD、中望CAD、浩辰CAD及类似兼容的CAD系统中的应用管理器。

command       function:
  pull        安装@lisp包 到 CAD
  install     安装@lisp Core 到 CAD
  list        列已安装的@lisp包
  remove      从本地CAD卸载 @lisp包
  search      联网搜索 @lisp 包

options:
  -h, --help  show this help message and exit
  -v, --version 显示当前安装的版本号
"""

def main():
    # target_function(*args,**kwargs)
    # path = pathlib.Path("pyproject.toml")
    # with  path.open(mode="rb") as  fp:
    #     projectdata=tomllib.load(fp)
        
    if len(sys.argv)>1:
        if sys.argv[1] ==  "pull":
            if len(sys.argv)>2:
                pull(sys.argv[2])
            else:
                print("Usage: atlisp pull pkgname")
                print("请指定包名 pkgname")
                print("示例: atlisp pull at-pm")
        if sys.argv[1] ==  "remove":
            if len(sys.argv)>2:
                pull(sys.argv[2])
            else:
                print("Usage: atlisp remove pkgname")
                print("请指定包名 pkgname")
                print("示例: atlisp remove at-pm")
        elif sys.argv[1]  ==  "install" or sys.argv[1]=="i":
            print("安装@lisp到CAD中")
            install_atlisp();
            print("......完成")
        elif sys.argv[1]  ==  "list" or sys.argv[1]=="l":
            print("已安装的应用包:")
            print("---------------")
            pkglist()
            print("===============")
        elif sys.argv[1]  ==  "search" or sys.argv[1]=="s":
            if len(sys.argv)>2:
                print("搜索  " + sys.argv[2])
                search(sys.argv[2])
            else:
                 print("Usage: atlisp search keystring")
                 print("请给出要搜索的关键字")
                 print("示例: atlisp search pdf")
        elif sys.argv[1]=="-h" or sys.argv[1]=="--help":
            print(help_str)
        elif sys.argv[1]=="-v" or sys.argv[1]=="--version":
            print("Version: "+  version)
        else:
            print("未知命令 "+ sys.argv[1])
    else:
        #parser.print_help()
        print(help_str)

    
