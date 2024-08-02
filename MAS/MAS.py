import tkinter
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil
import send2trash as trash
import datetime

WORK_FOLDER_PATH = os.path.dirname(__file__)+'/MAS/work'
USER_DESKTOP_PATH = os.path.expanduser('~')+'/Desktop'
EXPORT_WORK_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)),"work_archives")

class Window:
    def __init__(self) -> None:
        self.root = self.root = tkinter.Tk()
        self.root.title(u"Multi Agent System")
        w = self.root.winfo_screenwidth()-300
        h = self.root.winfo_screenheight()-330
        self.root.geometry("300x300+"+str(w)+"+"+str(h))
        self.root.configure(background='white')
        
        self.frame_folder = tkinter.Frame(self.root, relief=tkinter.FLAT, background='white')
        self.frame_folder.pack(fill=tkinter.BOTH, pady=10, padx=10)
        self.label_folder = tkinter.Label(self.frame_folder, text='作業フォルダ', font=('MSゴシック', '15', 'bold'), anchor=tkinter.NW, background='white')
        self.label_folder.pack(anchor=tkinter.NW)
        self.button_open = tkinter.Button(self.frame_folder, text='VSCodeで開く', font=('MSゴシック', '20'), padx=2, pady=2, relief=tkinter.RAISED, width=19, height=2, background='white', command=self.vscode_open)
        self.button_open.pack(anchor=tkinter.W, pady=5)
        self.button_change = tkinter.Button(self.frame_folder, text='work差替', font=('MSゴシック', '20'), padx=2, pady=2, width=8, background='white', command=self.workDir_change)
        self.button_change.pack(side=tkinter.LEFT)
        self.button_export = tkinter.Button(self.frame_folder, text='zipで出力', font=('MSゴシック', '20'), padx=2, pady=2, width=8, background='white', command=self.folder_export)
        self.button_export.pack(side=tkinter.LEFT)
        
        self.frame_run = tkinter.Frame(self.root, relief=tkinter.FLAT, background='white')
        self.frame_run.pack(fill=tkinter.BOTH, pady=10, padx=10)
        self.label_run = tkinter.Label(self.frame_run, text='マルチエージェントシステム', font=('MSゴシック', '15', 'bold'), anchor=tkinter.NW, background='white')
        self.label_run.pack(anchor=tkinter.NW)
        self.button_run = tkinter.Button(self.frame_run, text='実行', font=('MSゴシック', '20'), padx=2, pady=2, relief=tkinter.RAISED, width=19, height=2, background='white', command=self.MAS_run)
        self.button_run.pack(anchor=tkinter.W, pady=5)
        
        self.root.mainloop()
    
    def vscode_open(self):
        if os.path.isdir(WORK_FOLDER_PATH):
            subprocess.Popen(['code', '-n', WORK_FOLDER_PATH])
        else:
            tkinter.Tk().withdraw()
            messagebox.showinfo("ERROR","workフォルダがありません\n「work差替」からworkフォルダを設定してください")
        
    def workDir_change(self):
        work_path = filedialog.askdirectory(initialdir=USER_DESKTOP_PATH)
        if work_path == '':
            return
        if os.path.exists(WORK_FOLDER_PATH):
            trash.send2trash(WORK_FOLDER_PATH)
        shutil.copytree(work_path, WORK_FOLDER_PATH)
        
    def folder_export(self):
        now = datetime.datetime.now()
        shutil.make_archive(os.path.join(EXPORT_WORK_PATH,'archive_work_'+format(now, '%Y-%m-%d_%H-%M-%S')), format='zip', root_dir=WORK_FOLDER_PATH[:-len('/work')], base_dir='work')
        
    def MAS_run(self):
        self.close_terminal()
        applescript_code = f"""
            delay 1
            tell application "Terminal"
            activate
            do script "{WORK_FOLDER_PATH[:-len('MAS/work')]+'StartMAS.command'}"
            set bounds of front window to {0, 0, 400, 320}
            end tell
            """
        subprocess.Popen(["osascript", "-e", applescript_code])
        
    def close_terminal(self):
        applescript_code = """ tell application "Terminal"
                            set all_windows to every window
                            repeat with cur_window in all_windows
                                if name of cur_window contains "USER" then
                                    tell cur_window
                                        do script "end" in selected tab
                                        delay 2
                                    end tell
                                end if
                                if name of cur_window does not contain "MAS.command" then
                                    set tempID to id of cur_window
                                    tell the window id tempID to close
                                end if
                            end repeat
                        end tell """
        subprocess.Popen(["osascript", "-e", applescript_code])
        
if __name__ == '__main__':
    window = Window()
