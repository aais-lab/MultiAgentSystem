import tkinter
from tkinter import filedialog
import tkinter.messagebox as messagebox
import subprocess
import os
import shutil

WORK_FOLDER_PATH = os.path.dirname(__file__)+'/MAS/work'
USER_DESKTOP_PATH = os.path.expanduser('~')+'/Desktop'

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
        self.button_change = tkinter.Button(self.frame_folder, text='work差替', font=('MSゴシック', '20'), padx=2, pady=2, width=8, background='white', command=self.folder_change)
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
        
    def folder_change(self):
        folder_path = filedialog.askdirectory(initialdir=USER_DESKTOP_PATH)
        if folder_path == '':
            return
        if os.path.isfile(WORK_FOLDER_PATH):
            os.remove(WORK_FOLDER_PATH)
            shutil.move(folder_path, WORK_FOLDER_PATH)
            return
        shutil.rmtree(WORK_FOLDER_PATH)
        shutil.move(folder_path, WORK_FOLDER_PATH)
        
    def folder_export(self):
        shutil.make_archive('archive_work', format='zip', root_dir=WORK_FOLDER_PATH[:-len('/work')], base_dir='work')
        
    def MAS_run(self):
        applescript_code = f"""
            tell application "Terminal"
            activate
            do script "{WORK_FOLDER_PATH[:-len('MAS/work')]+'StartMAS.command'}"
            set bounds of front window to {0, 0, 400, 320}
            end tell
            """
        subprocess.Popen(["osascript", "-e", applescript_code])
        
if __name__ == '__main__':
    window = Window()
