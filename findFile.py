import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from fuzzywuzzy import fuzz

def find_files_and_dirs(directory, search_name, threshold=80, fuzzy=True, ignore_extension=False, prefix_match=False):
    matches = []
    file_count = 0
    for root, dirs, files in os.walk(directory):
        for name in files + dirs:
            file_count += 1
            if ignore_extension:
                name_without_ext = os.path.splitext(name)[0]
            else:
                name_without_ext = name

            if prefix_match:
                if name_without_ext.startswith(search_name):
                    matches.append((name, root, 100))
            elif fuzzy:
                match_ratio = fuzz.partial_ratio(name_without_ext, search_name)
                if match_ratio >= threshold:
                    matches.append((name, root, match_ratio))
            else:
                if search_name == name_without_ext:
                    matches.append((name, root, 100))
    return matches, file_count

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)

def search_files_and_dirs():
    directory = entry_directory.get()
    search_name = entry_search_name.get()
    threshold = int(entry_threshold.get())
    fuzzy = var_fuzzy.get()
    ignore_extension = var_ignore_extension.get()
    prefix_match = var_prefix_match.get()
    
    if not directory or not search_name:
        messagebox.showwarning("输入错误", "请填写所有字段")
        return
    
    # 启动一个新线程来执行搜索
    search_thread = threading.Thread(target=perform_search, args=(directory, search_name, threshold, fuzzy, ignore_extension, prefix_match))
    search_thread.start()

def perform_search(directory, search_name, threshold, fuzzy, ignore_extension, prefix_match):
    # 启动进度条
    progress_bar.start()
    
    results, file_count = find_files_and_dirs(directory, search_name, threshold, fuzzy, ignore_extension, prefix_match)
    
    # 停止进度条
    progress_bar.stop()
    
    # 更新UI需要在主线程中进行
    text_results.delete(1.0, tk.END)
    if results:
        for name, path, ratio in results:
            text_results.insert(tk.END, f"Found: {name} in {path} with match ratio: {ratio}\n")
    else:
        text_results.insert(tk.END, "No matches found.")
    
    # 更新文件数
    label_file_count.config(text=f"搜索的文件数: {file_count}")
    
    # 提示搜索完毕
    messagebox.showinfo("搜索完毕", "搜索已完成")

# 创建主窗口
root = tk.Tk()
root.title("模糊查找文件和文件夹")

# 创建并放置控件
label_directory = tk.Label(root, text="目录:")
label_directory.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

entry_directory = tk.Entry(root, width=50)
entry_directory.grid(row=0, column=1, padx=5, pady=5)

button_browse = tk.Button(root, text="浏览", command=browse_directory)
button_browse.grid(row=0, column=2, padx=5, pady=5)

label_search_name = tk.Label(root, text="文件名或文件夹名:")
label_search_name.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

entry_search_name = tk.Entry(root, width=50)
entry_search_name.grid(row=1, column=1, padx=5, pady=5)

label_threshold = tk.Label(root, text="匹配阈值:")
label_threshold.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

entry_threshold = tk.Entry(root, width=50)
entry_threshold.insert(0, "80")
entry_threshold.grid(row=2, column=1, padx=5, pady=5)

# 复选框用于开启模糊查询
var_fuzzy = tk.BooleanVar(value=True)
checkbox_fuzzy = tk.Checkbutton(root, text="开启模糊查询", variable=var_fuzzy)
checkbox_fuzzy.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

# 复选框用于忽略后缀名
var_ignore_extension = tk.BooleanVar(value=False)
checkbox_ignore_extension = tk.Checkbutton(root, text="忽略后缀名", variable=var_ignore_extension)
checkbox_ignore_extension.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

# 复选框用于前缀匹配
var_prefix_match = tk.BooleanVar(value=False)
checkbox_prefix_match = tk.Checkbutton(root, text="前缀匹配", variable=var_prefix_match)
checkbox_prefix_match.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)

button_search = tk.Button(root, text="搜索", command=search_files_and_dirs)
button_search.grid(row=4, column=1, padx=5, pady=5)

# 进度条
progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)

# 文件数标签
label_file_count = tk.Label(root, text="搜索的文件数: 0")
label_file_count.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

text_results = tk.Text(root, width=80, height=20)
text_results.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

# 运行主循环
root.mainloop()