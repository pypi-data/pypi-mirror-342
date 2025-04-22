import win32com.client,os
import time
install_str = '(progn(vl-load-com)(setq s strcat h "http" o(vlax-create-object (s"win"h".win"h"request.5.1"))v vlax-invoke e eval r read)(v o(quote open) "get" (s h"://atlisp.""cn/@"):vlax-true)(v o(quote send))(v o(quote WaitforResponse) 1000)(e(r(vlax-get-property o(quote ResponseText))))) '

def waitforcad(acadapp):
    while (not acadapp.GetAcadState().IsQuiescent):
        print(".",end="")
        time.sleep(1)
        
        
def install_atlisp():
    acadapp =win32com.client.Dispatch("AutoCAD.application")
    # 等待CAD忙完
    waitforcad(acadapp)
    acadapp.ActiveDocument.SendCommand('(setq @::backend-mode t) ')
    acadapp.ActiveDocument.SendCommand(install_str)
    acadapp.ActiveDocument.SendCommand("(@::set-config '@::tips-currpage 2) ")
    confirm = input("是否保持当前CAD实例，你可在当前实例中继续操作。(Y/N): ")
    if confirm.lower() in ['yes','y']:
        acadapp.visible=True
    else:
        acadapp.ActiveDocument.Close(False)
        acadapp.Quit()
    
def pull(pkgname):
    print("安装 `" + pkgname + "' 到CAD 中")
    acadapp =win32com.client.Dispatch("AutoCAD.application")
    # 等待CAD忙完
    print("正在初始化dwg,请稍等",end="")
    # 确定是否安装了@lisp core
    #acadapp.ActiveDocument.SendCommand(install_str)
    waitforcad(acadapp)
    time.sleep(3)
    acadapp.ActiveDocument.SendCommand('(progn(@::load-module "pkgman")(@::package-install "'+ pkgname +'")) ')
    print("\n正在安装 "+ pkgname+",请稍等",end="")
    waitforcad(acadapp)
    print("\n......完成")
    confirm = input("是否保持当前CAD实例，你可在当前实例中继续操作。(Y/N): ")
    if confirm.lower() in ['yes','y']:
        acadapp.visible=True
    else:
        acadapp.ActiveDocument.Close(False)
        acadapp.Quit()

def pkglist():
    "显示本地应用包"
    atlisp_config_path = os.path.join(os.path.expanduser(''),".atlisp") if os.name == 'posix' else os.path.join(os.environ['USERPROFILE'], '.atlisp')
    with open(os.path.join(atlisp_config_path,"pkg-in-use.lst"),"r") as pkglistfile:
        content = pkglistfile.read()
        print(content)

def search(keystring):
    print("联网搜索可用的应用包，开发中...")
    
def remove(pkgname):
    print("从本地CAD中卸载 `" + pkgname + "' 包")
    acadapp =win32com.client.Dispatch("AutoCAD.application")
    # 等待CAD忙完
    print("正在初始化dwg,请稍等",end="")
    # 确定是否安装了@lisp core
    #acadapp.ActiveDocument.SendCommand(install_str)
    waitforcad(acadapp)
    time.sleep(3)
    acadapp.ActiveDocument.SendCommand('(progn(@::package-remove "'+ pkgname +'")(if @::flag-menu-need-update (C:@m))) ')
    print("\n正在卸载 "+ pkgname+", 请稍等",end="")
    waitforcad(acadapp)
    print("\n......完成")
    confirm = input("是否保持当前CAD实例，你可在当前实例中继续操作。(Y/N): ")
    if confirm.lower() in ['yes','y']:
        acadapp.visible=True
    else:
        acadapp.ActiveDocument.Close(False)
        acadapp.Quit()
