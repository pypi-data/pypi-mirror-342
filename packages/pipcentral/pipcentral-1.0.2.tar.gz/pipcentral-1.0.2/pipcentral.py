import os
import sys
import shutil
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import pkg_resources
import subprocess
import threading
import csv
import requests
import json


try:
    import networkx as nx
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_DEPENDENCY_GRAPH = True
except ImportError:
    HAS_DEPENDENCY_GRAPH = False


VENVS_DIR = os.path.join(os.getcwd(), "venvs")
if not os.path.exists(VENVS_DIR):
    os.makedirs(VENVS_DIR)

LOCAL_REPO_DIR = os.path.join(os.getcwd(), "local_repo")
if not os.path.exists(LOCAL_REPO_DIR):
    os.makedirs(LOCAL_REPO_DIR)


BACKUP_DIR = os.path.join(os.getcwd(), "backups")
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)


class AdvancedPipManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Pipcentral")
        self.master.geometry("1300x950")
        
        self.style = ttk.Style(master)
        self.style.theme_use('clam')
        
        
        self.command_history = []  
        
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)
        
        
        self.create_header()

        self.create_installed_tab()
        self.create_manage_tab()
        self.create_advanced_features_tab()
        if HAS_DEPENDENCY_GRAPH:
            self.create_dependency_graph_tab()
        else:
            self.create_placeholder_tab("Dependency Graph", "Install networkx and matplotlib for dependency graph.")
        self.create_virtualenv_tab()
        self.create_env_comparison_tab()
        self.create_localrepo_tab()
        self.create_package_groups_tab()
        self.create_pip_command_builder_tab()
        self.create_command_history_tab()  
        self.create_scheduler_tab()          
        
        self.refresh_installed_packages()
        self.refresh_virtualenvs()
        self.refresh_env_comparison_options()
        self.refresh_package_groups()
        self.update_command_history_display()
        
        self.master.after(100, self.refresh_installed_packages)

    
    def create_header(self):
        
        header_frame = ttk.Frame(self.master)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        
        welcome_message = (
            "PipCentral is your one-stop tool for managing Python packages. "
            "With features like installed package management, virtual environments, "
            "local repository setup, pip scheduler, dependency graph visualization, and more, "
            "it’s a comprehensive solution for Python developers.\n"

            "Pipcentral © All Rights Reserved."
        )
        ttk.Label(header_frame, text=welcome_message, wraplength=600, justify="left").pack(side=tk.LEFT, padx=10)

    
    
    
    def add_to_command_history(self, cmd, output):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] Command: {' '.join(cmd)}\nOutput:\n{output}\n{'-'*40}\n"
        self.command_history.append(entry)
    
    def create_command_history_tab(self):
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="Command History")
        
        btn_frame = ttk.Frame(self.history_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_frame, text="Refresh History", command=self.update_command_history_display).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export History", command=self.export_history).pack(side=tk.LEFT, padx=5)
        
        self.history_text = scrolledtext.ScrolledText(self.history_frame, height=20)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def update_command_history_display(self):
        self.history_text.delete("1.0", tk.END)
        self.history_text.insert(tk.END, "\n".join(self.command_history))
    
    def export_history(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.command_history))
            messagebox.showinfo("Export", f"Command history exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    
    
    
    def run_pip_command(self, command, delay=0):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S")
        full_output = ""
        if delay:
            self.manage_output.insert(tk.END, f"Waiting for {delay} seconds before executing command...\n")
            self.manage_output.see(tk.END)
            time.sleep(delay)
        self.manage_output.insert(tk.END, f"Running command: {' '.join(command)}\n")
        self.manage_output.see(tk.END)
        self.manage_progress.start()
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                full_output += line
                self.manage_output.insert(tk.END, line)
                self.manage_output.see(tk.END)
            stdout, stderr = process.communicate()
            full_output += stdout + stderr
            if stdout:
                self.manage_output.insert(tk.END, stdout + "\n")
            if stderr:
                self.manage_output.insert(tk.END, stderr + "\n")
        except Exception as e:
            err_msg = f"Error: {e}\n"
            full_output += err_msg
            self.manage_output.insert(tk.END, err_msg)
        self.manage_progress.stop()
        self.manage_output.insert(tk.END, "Command finished.\n\n")
        self.manage_output.see(tk.END)
        self.refresh_installed_packages()
        
        self.add_to_command_history(command, full_output)
        self.update_command_history_display()
    
    
    
    
    
    def optimize_environment(self):
        
        self.advanced_output.insert(tk.END, "Optimizing Environment: Running pip check...\n")
        self.advanced_output.see(tk.END)
        try:
            process = subprocess.Popen(["pip", "check"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            output = stdout + "\n" + stderr
            self.advanced_output.insert(tk.END, output + "\n")
            self.add_to_command_history(["pip", "check"], output)
            if stdout.strip() == "":
                self.advanced_output.insert(tk.END, "No dependency conflicts detected.\n")
            else:
                self.advanced_output.insert(tk.END, "Dependency issues detected above. Consider upgrading or reinstalling conflicting packages.\n")
        except Exception as e:
            self.advanced_output.insert(tk.END, f"Optimize failed: {e}\n")
        self.advanced_output.see(tk.END)
    
    
    
    
    def create_scheduler_tab(self):
        self.scheduler_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scheduler_frame, text="Scheduler")
        
        
        backup_frame = ttk.LabelFrame(self.scheduler_frame, text="Schedule Environment Backup")
        backup_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(backup_frame, text="Delay (sec):").pack(side=tk.LEFT, padx=5)
        self.backup_delay_entry = ttk.Entry(backup_frame, width=10)
        self.backup_delay_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(backup_frame, text="Start Backup", command=self.schedule_backup).pack(side=tk.LEFT, padx=5)
        
        
        audit_frame = ttk.LabelFrame(self.scheduler_frame, text="Schedule Dependency Audit")
        audit_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(audit_frame, text="Delay (sec):").pack(side=tk.LEFT, padx=5)
        self.audit_delay_entry = ttk.Entry(audit_frame, width=10)
        self.audit_delay_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(audit_frame, text="Start Audit", command=self.schedule_dependency_audit).pack(side=tk.LEFT, padx=5)
        
        
        upgrade_frame = ttk.LabelFrame(self.scheduler_frame, text="Schedule Bulk Upgrade")
        upgrade_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(upgrade_frame, text="Delay (sec):").pack(side=tk.LEFT, padx=5)
        self.upgrade_delay_entry = ttk.Entry(upgrade_frame, width=10)
        self.upgrade_delay_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(upgrade_frame, text="Start Bulk Upgrade", command=self.schedule_bulk_upgrade).pack(side=tk.LEFT, padx=5)
        
        
        self.scheduler_output = scrolledtext.ScrolledText(self.scheduler_frame, height=10)
        self.scheduler_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def schedule_backup(self):
        try:
            delay = float(self.backup_delay_entry.get().strip())
        except:
            messagebox.showwarning("Input Error", "Enter a valid delay in seconds")
            return
        self.scheduler_output.insert(tk.END, f"Environment backup scheduled in {delay} seconds...\n")
        self.scheduler_output.see(tk.END)
        threading.Thread(target=self.delayed_backup, args=(delay,), daemon=True).start()
    
    def delayed_backup(self, delay):
        time.sleep(delay)
        self.backup_environments()
    
    def backup_environments(self):
        backup_logs = []
        envs = [env for env in os.listdir(VENVS_DIR) if os.path.isdir(os.path.join(VENVS_DIR, env))]
        for env in envs:
            env_path = os.path.join(VENVS_DIR, env)
            pip_path = self.get_env_pip_path(env_path)
            try:
                process = subprocess.Popen([pip_path, "freeze"],
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, _ = process.communicate()
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(BACKUP_DIR, f"{env}_backup_{timestamp}.txt")
                with open(backup_file, "w", encoding="utf-8") as f:
                    f.write(stdout)
                backup_logs.append(f"Backup for {env} saved to {backup_file}")
            except Exception as e:
                backup_logs.append(f"Backup for {env} failed: {e}")
        log_text = "\n".join(backup_logs)
        self.scheduler_output.insert(tk.END, log_text + "\n")
        self.scheduler_output.see(tk.END)
        self.add_to_command_history(["Backup Envs"], log_text)
    
    def schedule_dependency_audit(self):
        try:
            delay = float(self.audit_delay_entry.get().strip())
        except:
            messagebox.showwarning("Input Error", "Enter a valid delay in seconds")
            return
        self.scheduler_output.insert(tk.END, f"Dependency audit scheduled in {delay} seconds...\n")
        self.scheduler_output.see(tk.END)
        threading.Thread(target=self.delayed_audit, args=(delay,), daemon=True).start()
    
    def delayed_audit(self, delay):
        time.sleep(delay)
        self.dependency_audit()
    
    def dependency_audit(self):
        try:
            process = subprocess.Popen(["pip", "list", "--outdated"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            audit_result = stdout + "\n" + stderr
            self.scheduler_output.insert(tk.END, "Dependency Audit Result:\n" + audit_result + "\n")
            self.scheduler_output.see(tk.END)
            self.add_to_command_history(["pip", "list", "--outdated"], audit_result)
        except Exception as e:
            self.scheduler_output.insert(tk.END, f"Dependency audit failed: {e}\n")
            self.scheduler_output.see(tk.END)
    
    def schedule_bulk_upgrade(self):
        try:
            delay = float(self.upgrade_delay_entry.get().strip())
        except:
            messagebox.showwarning("Input Error", "Enter a valid delay in seconds")
            return
        self.scheduler_output.insert(tk.END, f"Bulk upgrade scheduled in {delay} seconds...\n")
        self.scheduler_output.see(tk.END)
        threading.Thread(target=self.delayed_bulk_upgrade, args=(delay,), daemon=True).start()
    
    def delayed_bulk_upgrade(self, delay):
        time.sleep(delay)
        self.bulk_upgrade()
    
    def bulk_upgrade(self):
        try:
            
            process = subprocess.Popen(["pip", "list", "--outdated"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, _ = process.communicate()
            outdated_packages = []
            for line in stdout.splitlines()[2:]:  
                if line.strip():
                    parts = line.split()
                    pkg = parts[0]
                    outdated_packages.append(pkg)
            upgrade_logs = []
            for pkg in outdated_packages:
                proc = subprocess.Popen(["pip", "install", "--upgrade", pkg],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out, err = proc.communicate()
                upgrade_logs.append(f"{pkg}: {out if out else err}")
            log_text = "\n".join(upgrade_logs)
            self.scheduler_output.insert(tk.END, "Bulk Upgrade Result:\n" + log_text + "\n")
            self.scheduler_output.see(tk.END)
            self.add_to_command_history(["Bulk Upgrade"], log_text)
            self.refresh_installed_packages()
        except Exception as e:
            self.scheduler_output.insert(tk.END, f"Bulk upgrade failed: {e}\n")
            self.scheduler_output.see(tk.END)
    
    
    
    
    
    
    
    
    
        
    def create_installed_tab(self):
        
        self.installed_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.installed_frame, text="Installed Packages")
        
        
        search_frame = ttk.Frame(self.installed_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        search_entry.bind("<KeyRelease>", self.filter_by_search)

        
        columns = ("Package", "Version", "Location")
        self.installed_tree = ttk.Treeview(self.installed_frame, columns=columns, show="headings")
        for col in columns:
            self.installed_tree.heading(col, text=col)
            self.installed_tree.column(col, anchor=tk.W, width=300)
        self.installed_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        
        self.installed_tree.bind("<Button-3>", self.popup_installed_context)
        self.installed_context_menu = tk.Menu(self.master, tearoff=0)
        self.installed_context_menu.add_command(label="View Details", command=self.show_package_details)
        self.installed_context_menu.add_command(label="Upgrade Package", command=self.context_upgrade)
        self.installed_context_menu.add_command(label="Uninstall Package", command=self.context_uninstall)
        self.installed_context_menu.add_command(label="Copy Info", command=self.context_copy)
        
        
        btn_frame = ttk.Frame(self.installed_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_installed_packages).pack(side=tk.LEFT, padx=5)

    def filter_by_search(self, event=None):
        
        search_term = self.search_var.get().lower()
        
        for row in self.installed_tree.get_children():
            self.installed_tree.delete(row)
        
        filtered_packages = [dist for dist in self.all_packages if search_term in dist.project_name.lower()]
        
        for dist in filtered_packages:
            self.installed_tree.insert("", tk.END, values=(dist.project_name, dist.version, dist.location))

    def popup_installed_context(self, event):
        region = self.installed_tree.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.installed_tree.identify_row(event.y)
            if row_id:
                self.installed_tree.selection_set(row_id)
                try:
                    self.installed_context_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    self.installed_context_menu.grab_release()

    def refresh_installed_packages(self):
        
        for row in self.installed_tree.get_children():
            self.installed_tree.delete(row)
        self.all_packages = sorted(pkg_resources.working_set, key=lambda d: d.project_name.lower())
        for dist in self.all_packages:
            self.installed_tree.insert("", tk.END, values=(dist.project_name, dist.version, dist.location))

    def show_package_details(self):
        selected = self.installed_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a package first.")
            return
        item = self.installed_tree.item(selected[0])
        pkg_name = item['values'][0]
        try:
            dist = pkg_resources.get_distribution(pkg_name)
            details = f"Name: {dist.project_name}\nVersion: {dist.version}\nLocation: {dist.location}\n"
            metadata = ""
            if dist.has_metadata("METADATA"):
                metadata = dist.get_metadata("METADATA")
            elif dist.has_metadata("PKG-INFO"):
                metadata = dist.get_metadata("PKG-INFO")
            summary = "No summary available."
            for line in metadata.splitlines():
                if line.startswith("Summary:"):
                    summary = line.split(":", 1)[1].strip()
                    break
            details += f"Summary: {summary}"
            messagebox.showinfo("Package Details", details)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def context_upgrade(self):
        selected = self.installed_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a package to upgrade.")
            return
        pkg_name = self.installed_tree.item(selected[0])['values'][0]
        threading.Thread(target=self.run_pip_command, args=(["pip", "install", "--upgrade", pkg_name], 0), daemon=True).start()

    def context_uninstall(self):
        selected = self.installed_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a package to uninstall.")
            return
        pkg_name = self.installed_tree.item(selected[0])['values'][0]
        if not messagebox.askyesno("Confirm", f"Are you sure you want to uninstall {pkg_name}?"):
            return
        threading.Thread(target=self.run_pip_command, args=(["pip", "uninstall", "-y", pkg_name], 0), daemon=True).start()

    def context_copy(self):
        selected = self.installed_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a package to copy info.")
            return
        pkg, ver, loc = self.installed_tree.item(selected[0])['values']
        info_text = f"{pkg}=={ver}\nLocation: {loc}"
        self.master.clipboard_clear()
        self.master.clipboard_append(info_text)
        messagebox.showinfo("Copied", "Package info copied to clipboard.")

    
    
    
    def create_manage_tab(self):
        self.manage_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.manage_frame, text="Manage Package")
        
        
        ttk.Label(self.manage_frame, text="Enter package name:").pack(pady=5)
        self.manage_entry = ttk.Entry(self.manage_frame, width=50)
        self.manage_entry.pack(pady=5)
        
        
        version_frame = ttk.Frame(self.manage_frame)
        version_frame.pack(pady=5)
        ttk.Label(version_frame, text="Version (optional):").pack(side=tk.LEFT, padx=5)
        self.version_entry = ttk.Entry(version_frame, width=20)
        self.version_entry.pack(side=tk.LEFT)
        
        
        delay_frame = ttk.Frame(self.manage_frame)
        delay_frame.pack(pady=5)
        ttk.Label(delay_frame, text="Delay (seconds):").pack(side=tk.LEFT, padx=5)
        self.delay_entry = ttk.Entry(delay_frame, width=10)
        self.delay_entry.pack(side=tk.LEFT)
        
        
        extra_frame = ttk.Frame(self.manage_frame)
        extra_frame.pack(pady=5)
        ttk.Label(extra_frame, text="Extra pip options (optional):").pack(side=tk.LEFT, padx=5)
        self.extra_options_entry = ttk.Entry(extra_frame, width=50)
        self.extra_options_entry.pack(side=tk.LEFT)
        
        
        verbose_frame = ttk.Frame(self.manage_frame)
        verbose_frame.pack(pady=5)
        self.verbose_var = tk.BooleanVar()
        ttk.Checkbutton(verbose_frame, text="Verbose Output", variable=self.verbose_var).pack(side=tk.LEFT, padx=5)
        
        
        dry_run_frame = ttk.Frame(self.manage_frame)
        dry_run_frame.pack(pady=5)
        self.dry_run_var = tk.BooleanVar()
        ttk.Checkbutton(dry_run_frame, text="Dry Run (simulate command)", variable=self.dry_run_var).pack(side=tk.LEFT, padx=5)
        
        
        btn_frame = ttk.Frame(self.manage_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Install", command=self.install_package).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Uninstall", command=self.uninstall_package).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Upgrade", command=self.upgrade_package).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel_operation).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="History", command=self.show_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        
        
        self.manage_progress = ttk.Progressbar(self.manage_frame, mode="indeterminate")
        self.manage_progress.pack(fill=tk.X, padx=10, pady=5)
        
        
        self.manage_output = scrolledtext.ScrolledText(self.manage_frame, height=15)
        self.manage_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def install_package(self):
        pkg = self.manage_entry.get().strip()
        if not pkg:
            messagebox.showwarning("Input Required", "Please enter a package name to install.")
            return
        
        version = self.version_entry.get().strip()
        if version:
            pkg = f"{pkg}=={version}"
        delay = self.get_delay_seconds()
        
        command = ["pip", "install"]
        if self.verbose_var.get():
            command.append("-v")
        
        extra_opts = self.extra_options_entry.get().strip()
        if extra_opts:
            command.extend(extra_opts.split())
        command.append(pkg)
        threading.Thread(target=self.run_pip_command, args=(command, delay), daemon=True).start()
        
    def uninstall_package(self):
        pkg = self.manage_entry.get().strip()
        if not pkg:
            messagebox.showwarning("Input Required", "Please enter a package name to uninstall.")
            return
        if not messagebox.askyesno("Confirm", f"Are you sure you want to uninstall {pkg}?"):
            return
        delay = self.get_delay_seconds()
        
        command = ["pip", "uninstall", "-y", pkg]
        if self.verbose_var.get():
            command.insert(1, "-v")  
        extra_opts = self.extra_options_entry.get().strip()
        if extra_opts:
            command[1:1] = extra_opts.split()
        threading.Thread(target=self.run_pip_command, args=(command, delay), daemon=True).start()
        
    def upgrade_package(self):
        pkg = self.manage_entry.get().strip()
        if not pkg:
            messagebox.showwarning("Input Required", "Please enter a package name to upgrade.")
            return
        delay = self.get_delay_seconds()
        
        command = ["pip", "install", "--upgrade", pkg]
        if self.verbose_var.get():
            command.insert(1, "-v")
        extra_opts = self.extra_options_entry.get().strip()
        if extra_opts:
            command[1:1] = extra_opts.split()
        threading.Thread(target=self.run_pip_command, args=(command, delay), daemon=True).start()
        
    def get_delay_seconds(self):
        try:
            delay = float(self.delay_entry.get().strip())
            return delay if delay > 0 else 0
        except Exception:
            return 0

    def run_pip_command(self, command, delay):
        self.manage_progress.start()
        command_str = " ".join(command)
        
        self.command_history.append(command_str)
        self.manage_output.insert(tk.END, f"Running: {command_str}\n")
        self.manage_output.see(tk.END)
        
        
        if self.dry_run_var.get():
            self.manage_output.insert(tk.END, "Dry Run selected: Command not executed.\n")
            self.manage_progress.stop()
            return
        
        if delay > 0:
            time.sleep(delay)
            
        try:
            self.current_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            for line in self.current_process.stdout:
                self.manage_output.insert(tk.END, line)
                self.manage_output.see(tk.END)
            
            err = self.current_process.stderr.read()
            if err:
                self.manage_output.insert(tk.END, err)
        except Exception as e:
            self.manage_output.insert(tk.END, f"Error: {e}\n")
        finally:
            self.manage_progress.stop()
            self.current_process = None

    def cancel_operation(self):
        
        if self.current_process:
            try:
                self.current_process.terminate()
                self.manage_output.insert(tk.END, "Process terminated by user.\n")
            except Exception as e:
                self.manage_output.insert(tk.END, f"Error terminating process: {e}\n")
            self.current_process = None
        else:
            messagebox.showinfo("Cancel", "No running operation to cancel.")

    def show_history(self):
        
        history_window = tk.Toplevel(self.manage_frame)
        history_window.title("Command History")
        history_text = scrolledtext.ScrolledText(history_window, width=80, height=20)
        history_text.pack(fill=tk.BOTH, expand=True)
        history_text.insert(tk.END, "\n".join(self.command_history))
        history_text.config(state=tk.DISABLED)

    def clear_output(self):
        self.manage_output.delete("1.0", tk.END)

    
    def create_advanced_features_tab(self):
        self.advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_frame, text="Advanced Features")
        
        btn_frame = ttk.Frame(self.advanced_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Check Outdated Packages", command=self.check_outdated_packages).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Show Pip Version", command=self.show_pip_version).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Pip", command=self.update_pip).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Scan Vulnerabilities", command=self.scan_vulnerabilities).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Generate Optimized Requirements", command=self.generate_optimized_requirements).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cleanup Dependencies", command=self.cleanup_dependencies).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Optimize Environment", command=self.optimize_environment).pack(side=tk.LEFT, padx=5)
        
        self.advanced_output = scrolledtext.ScrolledText(self.advanced_frame, height=15)
        self.advanced_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def check_outdated_packages(self):
        threading.Thread(target=self.run_outdated_command, daemon=True).start()
    
    def run_outdated_command(self):
        self.advanced_output.insert(tk.END, "Checking for outdated packages...\n")
        self.advanced_output.see(tk.END)
        try:
            process = subprocess.Popen(["pip", "list", "--outdated"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout:
                self.advanced_output.insert(tk.END, stdout + "\n")
            if stderr:
                self.advanced_output.insert(tk.END, stderr + "\n")
        except Exception as e:
            self.advanced_output.insert(tk.END, f"Error: {e}\n")
        self.advanced_output.insert(tk.END, "Finished checking outdated packages.\n\n")
        self.advanced_output.see(tk.END)
    
    def show_pip_version(self):
        threading.Thread(target=self.run_pip_version, daemon=True).start()
    
    def run_pip_version(self):
        self.advanced_output.insert(tk.END, "Retrieving pip version...\n")
        self.advanced_output.see(tk.END)
        try:
            process = subprocess.Popen(["pip", "--version"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout:
                self.advanced_output.insert(tk.END, stdout + "\n")
            if stderr:
                self.advanced_output.insert(tk.END, stderr + "\n")
        except Exception as e:
            self.advanced_output.insert(tk.END, f"Error: {e}\n")
        self.advanced_output.insert(tk.END, "Finished retrieving pip version.\n\n")
        self.advanced_output.see(tk.END)
    
    def update_pip(self):
        if not messagebox.askyesno("Confirm", "Update pip to the latest version?"):
            return
        threading.Thread(target=self.run_update_pip, daemon=True).start()
    
    def run_update_pip(self):
        self.advanced_output.insert(tk.END, "Updating pip...\n")
        self.advanced_output.see(tk.END)
        try:
            process = subprocess.Popen(["python", "-m", "pip", "install", "--upgrade", "pip"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout:
                self.advanced_output.insert(tk.END, stdout + "\n")
            if stderr:
                self.advanced_output.insert(tk.END, stderr + "\n")
        except Exception as e:
            self.advanced_output.insert(tk.END, f"Error: {e}\n")
        self.advanced_output.insert(tk.END, "Finished updating pip.\n\n")
        self.advanced_output.see(tk.END)
    
    def scan_vulnerabilities(self):
        threading.Thread(target=self.run_scan_vulnerabilities, daemon=True).start()
    
    def run_scan_vulnerabilities(self):
        self.advanced_output.insert(tk.END, "Scanning for vulnerabilities...\n")
        self.advanced_output.see(tk.END)
        try:
            process = subprocess.Popen(["pip-audit"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout:
                self.advanced_output.insert(tk.END, stdout + "\n")
            if stderr:
                self.advanced_output.insert(tk.END, stderr + "\n")
        except Exception as e:
            self.advanced_output.insert(tk.END, f"Error (pip-audit might not be installed): {e}\n")
        self.advanced_output.insert(tk.END, "Finished vulnerability scan.\n\n")
        self.advanced_output.see(tk.END)
    
    def generate_optimized_requirements(self):
        threading.Thread(target=self.run_generate_optimized, daemon=True).start()
    
    def run_generate_optimized(self):
        self.advanced_output.insert(tk.END, "Generating optimized requirements using pip-compile...\n")
        self.advanced_output.see(tk.END)
        try:
            process = subprocess.Popen(["pip-compile", "requirements.in"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout:
                self.advanced_output.insert(tk.END, stdout + "\n")
            if stderr:
                self.advanced_output.insert(tk.END, stderr + "\n")
        except Exception as e:
            self.advanced_output.insert(tk.END, f"Error (pip-compile might not be installed): {e}\n")
        self.advanced_output.insert(tk.END, "Finished generating optimized requirements.\n\n")
        self.advanced_output.see(tk.END)
    
    def cleanup_dependencies(self):
        threading.Thread(target=self.run_cleanup_dependencies, daemon=True).start()
    
    def run_cleanup_dependencies(self):
        self.advanced_output.insert(tk.END, "Cleaning up unused dependencies...\n")
        self.advanced_output.see(tk.END)
        pkg = self.manage_entry.get().strip()  
        if not pkg:
            self.advanced_output.insert(tk.END, "Provide a package name in Manage Package tab for cleanup.\n")
            return
        try:
            process = subprocess.Popen(["pip-autoremove", pkg, "-y"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout:
                self.advanced_output.insert(tk.END, stdout + "\n")
            if stderr:
                self.advanced_output.insert(tk.END, stderr + "\n")
        except Exception as e:
            self.advanced_output.insert(tk.END, f"Error (pip-autoremove might not be installed): {e}\n")
        self.advanced_output.insert(tk.END, "Finished cleanup.\n\n")
        self.advanced_output.see(tk.END)
    
    
    def create_dependency_graph_tab(self):
        self.depgraph_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.depgraph_frame, text="Dependency Graph")
        
        top_frame = ttk.Frame(self.depgraph_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(top_frame, text="Enter package name (leave blank for all):").pack(side=tk.LEFT)
        self.dep_entry = ttk.Entry(top_frame, width=30)
        self.dep_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Generate Graph", command=self.generate_dependency_graph).pack(side=tk.LEFT, padx=5)
        
        self.canvas_frame = ttk.Frame(self.depgraph_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.dep_message = ttk.Label(self.canvas_frame, text="Click 'Generate Graph' to display dependencies.")
        self.dep_message.pack()
    
    def generate_dependency_graph(self):
        pkg_name = self.dep_entry.get().strip()
        G = nx.DiGraph()
        processed = set()
        if pkg_name:
            try:
                self.build_dependency_tree(pkg_name, G, processed)
            except Exception as e:
                messagebox.showerror("Error", f"Error generating dependency graph: {e}")
                return
        else:
            for dist in pkg_resources.working_set:
                pname = dist.project_name
                G.add_node(pname)
                for req in dist.requires():
                    req_name = req.project_name
                    G.add_edge(pname, req_name)
        if G.number_of_nodes() == 0:
            messagebox.showinfo("No Dependencies", "No dependency information available.")
            return
        labels = {}
        for node in G.nodes():
            license_info = "N/A"
            try:
                dist = pkg_resources.get_distribution(node)
                metadata = ""
                if dist.has_metadata("METADATA"):
                    metadata = dist.get_metadata("METADATA")
                elif dist.has_metadata("PKG-INFO"):
                    metadata = dist.get_metadata("PKG-INFO")
                for line in metadata.splitlines():
                    if line.startswith("License:"):
                        license_info = line.split(":", 1)[1].strip()
                        break
            except Exception:
                pass
            labels[node] = f"{node}\n({license_info})"
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        fig = plt.Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.set_title("Dependency Graph")
        try:
            pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        except Exception as e:
            print("Graphviz layout failed. Falling back to spring layout.", e)
            pos = nx.spring_layout(G, k=0.5)
        nx.draw_networkx(G, pos, ax=ax, labels=labels,
                         node_color="lightblue", edge_color="gray", font_size=8)
        x_vals, y_vals = zip(*pos.values())
        padding_x = (max(x_vals) - min(x_vals)) * 0.25
        padding_y = (max(y_vals) - min(y_vals)) * 0.25
        ax.set_xlim(min(x_vals) - padding_x, max(x_vals) + padding_x)
        ax.set_ylim(min(y_vals) - padding_y, max(y_vals) + padding_y)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()
    
    def build_dependency_tree(self, pkg_name, graph, processed):
        if pkg_name in processed:
            return
        processed.add(pkg_name)
        try:
            dist = pkg_resources.get_distribution(pkg_name)
        except Exception:
            return
        graph.add_node(pkg_name)
        for req in dist.requires():
            req_name = req.project_name
            graph.add_edge(pkg_name, req_name)
            self.build_dependency_tree(req_name, graph, processed)
    
    
    def create_virtualenv_tab(self):
        self.venv_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.venv_frame, text="Virtual Env Manager")
        
        top_frame = ttk.Frame(self.venv_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(top_frame, text="Environment Name:").pack(side=tk.LEFT)
        self.venv_entry = ttk.Entry(top_frame, width=30)
        self.venv_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(top_frame, text="Python Interpreter:").pack(side=tk.LEFT, padx=5)
        self.python_interpreter_entry = ttk.Entry(top_frame, width=20)
        self.python_interpreter_entry.insert(0, sys.executable)
        self.python_interpreter_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Create Environment", command=self.create_virtualenv).pack(side=tk.LEFT, padx=5)
        
        list_frame = ttk.Frame(self.venv_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        ttk.Label(list_frame, text="Available Environments:").pack(anchor=tk.W)
        self.venv_listbox = tk.Listbox(list_frame, height=8)
        self.venv_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.venv_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.venv_listbox.config(yscrollcommand=scrollbar.set)
        
        btn_frame = ttk.Frame(self.venv_frame)
        btn_frame.pack(padx=10, pady=5)
        ttk.Button(btn_frame, text="Refresh Environments", command=self.refresh_virtualenvs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected Env", command=self.delete_virtualenv).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export Requirements", command=self.export_requirements).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Import Requirements", command=self.import_requirements).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Health Check", command=self.health_check_env).pack(side=tk.LEFT, padx=5)
    
    def create_virtualenv(self):
        env_name = self.venv_entry.get().strip()
        if not env_name:
            messagebox.showwarning("Input Required", "Please enter a name for the virtual environment.")
            return
        env_path = os.path.join(VENVS_DIR, env_name)
        if os.path.exists(env_path):
            messagebox.showwarning("Exists", "A virtual environment with this name already exists.")
            return
        interpreter = self.python_interpreter_entry.get().strip() or "python"
        threading.Thread(target=self.run_create_virtualenv, args=(env_path, interpreter), daemon=True).start()
    
    def run_create_virtualenv(self, env_path, interpreter):
        self.show_info_in_venv_output(f"Creating virtual environment at {env_path} using {interpreter}...\n")
        try:
            process = subprocess.Popen([interpreter, "-m", "venv", env_path],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            output = (stdout if stdout else "") + (stderr if stderr else "")
            self.show_info_in_venv_output(output)
        except Exception as e:
            self.show_info_in_venv_output(f"Error: {e}\n")
        self.refresh_virtualenvs()
    
    def refresh_virtualenvs(self):
        self.venv_listbox.delete(0, tk.END)
        try:
            envs = [d for d in os.listdir(VENVS_DIR) if os.path.isdir(os.path.join(VENVS_DIR, d))]
            for env in sorted(envs):
                self.venv_listbox.insert(tk.END, env)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list virtual environments: {e}")
    
    def delete_virtualenv(self):
        selected = self.venv_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an environment to delete.")
            return
        env_name = self.venv_listbox.get(selected[0])
        env_path = os.path.join(VENVS_DIR, env_name)
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the environment '{env_name}'?"):
            try:
                shutil.rmtree(env_path)
                messagebox.showinfo("Deleted", f"Environment '{env_name}' has been deleted.")
                self.refresh_virtualenvs()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete environment: {e}")
    
    def export_requirements(self):
        selected = self.venv_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select an environment to export requirements.")
            return
        env_name = self.venv_listbox.get(selected[0])
        env_path = os.path.join(VENVS_DIR, env_name)
        pip_path = self.get_env_pip_path(env_path)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Export Requirements",
                                                 filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        try:
            process = subprocess.Popen([pip_path, "freeze"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, _ = process.communicate()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(stdout)
            messagebox.showinfo("Exported", f"Requirements exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export requirements: {e}")
    
    def import_requirements(self):
        selected = self.venv_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select an environment to import requirements.")
            return
        env_name = self.venv_listbox.get(selected[0])
        env_path = os.path.join(VENVS_DIR, env_name)
        pip_path = self.get_env_pip_path(env_path)
        file_path = filedialog.askopenfilename(title="Import Requirements",
                                               filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return
        try:
            process = subprocess.Popen([pip_path, "install", "-r", file_path],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            messagebox.showinfo("Imported", f"Requirements imported:\n{stdout}\n{stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import requirements: {e}")
    
    def health_check_env(self):
        selected = self.venv_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select an environment for health check.")
            return
        env_name = self.venv_listbox.get(selected[0])
        env_path = os.path.join(VENVS_DIR, env_name)
        pip_path = self.get_env_pip_path(env_path)
        def run_check():
            try:
                process = subprocess.Popen([pip_path, "check"],
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                result = stdout if stdout else stderr
                messagebox.showinfo("Environment Health Check", result)
            except Exception as e:
                messagebox.showerror("Error", f"Health check failed: {e}")
        threading.Thread(target=run_check, daemon=True).start()
    
    def get_env_pip_path(self, env_path):
        if os.name == 'nt':
            return os.path.join(env_path, "Scripts", "pip.exe")
        else:
            return os.path.join(env_path, "bin", "pip")
    
    def show_info_in_venv_output(self, text):
        messagebox.showinfo("Virtual Environment Manager", text)
    
    
    def create_env_comparison_tab(self):
        self.env_comp_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.env_comp_frame, text="Env Comparison")
        
        comp_top = ttk.Frame(self.env_comp_frame)
        comp_top.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(comp_top, text="Select Env A:").pack(side=tk.LEFT, padx=5)
        self.env_a_combo = ttk.Combobox(comp_top, state="readonly", width=20)
        self.env_a_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(comp_top, text="Select Env B:").pack(side=tk.LEFT, padx=5)
        self.env_b_combo = ttk.Combobox(comp_top, state="readonly", width=20)
        self.env_b_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(comp_top, text="Compare Environments", command=self.compare_envs).pack(side=tk.LEFT, padx=5)
        
        self.env_comp_output = scrolledtext.ScrolledText(self.env_comp_frame, height=15)
        self.env_comp_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def refresh_env_comparison_options(self):
        try:
            envs = [d for d in os.listdir(VENVS_DIR) if os.path.isdir(os.path.join(VENVS_DIR, d))]
            envs_sorted = sorted(envs)
            self.env_a_combo['values'] = envs_sorted
            self.env_b_combo['values'] = envs_sorted
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load environments: {e}")
    
    def compare_envs(self):
        env_a = self.env_a_combo.get()
        env_b = self.env_b_combo.get()
        if not env_a or not env_b:
            messagebox.showwarning("Input Required", "Please select both environments.")
            return
        env_a_path = os.path.join(VENVS_DIR, env_a)
        env_b_path = os.path.join(VENVS_DIR, env_b)
        pip_a = self.get_env_pip_path(env_a_path)
        pip_b = self.get_env_pip_path(env_b_path)
        try:
            proc_a = subprocess.Popen([pip_a, "freeze"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out_a, _ = proc_a.communicate()
            
            proc_b = subprocess.Popen([pip_b, "freeze"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out_b, _ = proc_b.communicate()
            
            pkgs_a = set(out_a.splitlines())
            pkgs_b = set(out_b.splitlines())
            
            only_a = pkgs_a - pkgs_b
            only_b = pkgs_b - pkgs_a
            common = pkgs_a & pkgs_b
            
            result_text = "Packages only in Env A:\n" + "\n".join(sorted(only_a)) + "\n\n"
            result_text += "Packages only in Env B:\n" + "\n".join(sorted(only_b)) + "\n\n"
            result_text += "Common Packages:\n" + "\n".join(sorted(common)) + "\n\n"
            
            self.env_comp_output.delete("1.0", tk.END)
            self.env_comp_output.insert(tk.END, result_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error comparing environments: {e}")
    
    
    def create_localrepo_tab(self):
        
        self.localrepo_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.localrepo_frame, text="Local Repo")
        
        
        top_frame = ttk.Frame(self.localrepo_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(top_frame, text="Package name to download:").pack(side=tk.LEFT, padx=5)
        self.localrepo_entry = ttk.Entry(top_frame, width=30)
        self.localrepo_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Download Package", command=self.download_package_to_localrepo).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Refresh Repo List", command=self.refresh_local_repo).pack(side=tk.LEFT, padx=5)
        
        
        self.localrepo_listbox = tk.Listbox(self.localrepo_frame, height=10)
        self.localrepo_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        bottom_frame = ttk.Frame(self.localrepo_frame)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(bottom_frame, text="Install from Local Repo", command=self.install_from_local_repo).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Delete Package", command=self.delete_package).pack(side=tk.LEFT, padx=5)
        self.progress = ttk.Progressbar(bottom_frame, mode="indeterminate")
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        
        log_frame = ttk.Labelframe(self.localrepo_frame, text="Operation Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.log_text = tk.Text(log_frame, height=8, state="disabled", wrap="word")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Button(log_frame, text="Clear Log", command=self.clear_log).pack(padx=5, pady=5)
        
        self.refresh_local_repo()


    def log_message(self, message):
        """Append messages to the log pane."""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)


    def clear_log(self):
        """Clears the operation log."""
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")


    def download_package_to_localrepo(self):
        pkg = self.localrepo_entry.get().strip()
        if not pkg:
            messagebox.showwarning("Input Required", "Please enter a package name to download.")
            return
        
        threading.Thread(target=self.run_download_localrepo, args=(pkg,), daemon=True).start()


    def run_download_localrepo(self, pkg):
        try:
            self.progress.start()
            self.log_message(f"Downloading package: {pkg}")
            process = subprocess.Popen(
                ["pip", "download", pkg, "-d", LOCAL_REPO_DIR],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            stdout, stderr = process.communicate()
            result = stdout + "\n" + stderr
            self.log_message("Download results:\n" + result)
            messagebox.showinfo("Download", result)
            self.refresh_local_repo()
        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {e}")
            self.log_message(f"Error downloading package {pkg}: {e}")
        finally:
            self.progress.stop()


    def refresh_local_repo(self):
        self.localrepo_listbox.delete(0, tk.END)
        try:
            files = os.listdir(LOCAL_REPO_DIR)
            for f in files:
                self.localrepo_listbox.insert(tk.END, f)
            self.log_message("Local repository refreshed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list local repository: {e}")
            self.log_message(f"Error refreshing local repository: {e}")


    def install_from_local_repo(self):
        selected = self.localrepo_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a package file to install.")
            return
        filename = self.localrepo_listbox.get(selected[0])
        pkg_path = os.path.join(LOCAL_REPO_DIR, filename)
        threading.Thread(target=self.run_install_from_local, args=(pkg_path,), daemon=True).start()


    def run_install_from_local(self, pkg_path):
        try:
            self.progress.start()
            self.log_message(f"Installing package from: {pkg_path}")
            process = subprocess.Popen(
                ["pip", "install", pkg_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            stdout, stderr = process.communicate()
            result = stdout + "\n" + stderr
            self.log_message("Installation results:\n" + result)
            messagebox.showinfo("Install from Local Repo", result)
        except Exception as e:
            messagebox.showerror("Error", f"Installation failed: {e}")
            self.log_message(f"Error installing package from {pkg_path}: {e}")
        finally:
            self.progress.stop()


    def delete_package(self):
        selected = self.localrepo_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a package file to delete.")
            return
        filename = self.localrepo_listbox.get(selected[0])
        pkg_path = os.path.join(LOCAL_REPO_DIR, filename)
        if messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete {filename}?"):
            try:
                os.remove(pkg_path)
                self.log_message(f"Deleted package file: {filename}")
                self.refresh_local_repo()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete {filename}: {e}")
                self.log_message(f"Error deleting package {filename}: {e}")

    
    
    def create_package_groups_tab(self):
        self.package_groups_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.package_groups_frame, text="Package Groups")
        
        group_frame = ttk.Frame(self.package_groups_frame)
        group_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(group_frame, text="Group Name:").pack(side=tk.LEFT, padx=5)
        self.group_name_entry = ttk.Entry(group_frame, width=20)
        self.group_name_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(group_frame, text="Packages (comma separated):").pack(side=tk.LEFT, padx=5)
        self.group_packages_entry = ttk.Entry(group_frame, width=40)
        self.group_packages_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(group_frame, text="Add Group", command=self.add_package_group).pack(side=tk.LEFT, padx=5)
        
        list_frame = ttk.Frame(self.package_groups_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        ttk.Label(list_frame, text="Saved Package Groups:").pack(anchor=tk.W)
        self.group_listbox = tk.Listbox(list_frame, height=8)
        self.group_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.group_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.group_listbox.config(yscrollcommand=scrollbar.set)
        
        btn_frame = ttk.Frame(self.package_groups_frame)
        btn_frame.pack(padx=10, pady=5)
        ttk.Button(btn_frame, text="Install Selected Group", command=self.install_group).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Selected Group", command=self.delete_group).pack(side=tk.LEFT, padx=5)
        
        self.package_groups = {}
    
    def add_package_group(self):
        group_name = self.group_name_entry.get().strip()
        pkg_list_str = self.group_packages_entry.get().strip()
        if not group_name or not pkg_list_str:
            messagebox.showwarning("Input Required", "Provide both group name and package list.")
            return
        packages = [pkg.strip() for pkg in pkg_list_str.split(",") if pkg.strip()]
        self.package_groups[group_name] = packages
        self.refresh_package_groups()
        self.group_name_entry.delete(0, tk.END)
        self.group_packages_entry.delete(0, tk.END)
    
    def refresh_package_groups(self):
        self.group_listbox.delete(0, tk.END)
        for group_name, packages in self.package_groups.items():
            display = f"{group_name}: {', '.join(packages)}"
            self.group_listbox.insert(tk.END, display)
    
    def install_group(self):
        selected = self.group_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a group to install.")
            return
        group_entry = self.group_listbox.get(selected[0])
        group_name = group_entry.split(":")[0].strip()
        packages = self.package_groups.get(group_name, [])
        if not packages:
            messagebox.showinfo("Empty Group", "No packages found in the selected group.")
            return
        cmd = ["pip", "install"] + packages
        threading.Thread(target=self.run_pip_command_group, args=(cmd,), daemon=True).start()
    
    def run_pip_command_group(self, command):
        try:
            process = subprocess.Popen(command,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            result = stdout + "\n" + stderr
            messagebox.showinfo("Install Group", result)
        except Exception as e:
            messagebox.showerror("Error", f"Error installing group: {e}")
    
    def delete_group(self):
        selected = self.group_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a group to delete.")
            return
        group_entry = self.group_listbox.get(selected[0])
        group_name = group_entry.split(":")[0].strip()
        if group_name in self.package_groups:
            del self.package_groups[group_name]
        self.refresh_package_groups()
    
    
    def create_pip_command_builder_tab(self):
        self.pip_builder_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pip_builder_frame, text="Pip Command Builder")
        
        top_frame = ttk.Frame(self.pip_builder_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        
        ttk.Label(top_frame, text="Package Name:").pack(side=tk.LEFT, padx=5)
        self.builder_pkg_entry = ttk.Entry(top_frame, width=20)
        self.builder_pkg_entry.pack(side=tk.LEFT, padx=5)
        
        
        ttk.Label(top_frame, text="Index URL:").pack(side=tk.LEFT, padx=5)
        self.builder_index_entry = ttk.Entry(top_frame, width=20)
        self.builder_index_entry.pack(side=tk.LEFT, padx=5)
        
        
        ttk.Label(top_frame, text="Venv Name:").pack(side=tk.LEFT, padx=5)
        self.builder_venv_entry = ttk.Entry(top_frame, width=15)
        self.builder_venv_entry.pack(side=tk.LEFT, padx=5)
        
        
        self.builder_install_var = tk.BooleanVar()
        self.builder_upgrade_var = tk.BooleanVar()
        self.builder_no_deps_var = tk.BooleanVar()
        self.builder_user_var = tk.BooleanVar()
        self.builder_dry_run_var = tk.BooleanVar()
        self.builder_offline_var = tk.BooleanVar()
        
        ttk.Checkbutton(top_frame, text="Install", variable=self.builder_install_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(top_frame, text="Upgrade", variable=self.builder_upgrade_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(top_frame, text="No-deps", variable=self.builder_no_deps_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(top_frame, text="User", variable=self.builder_user_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(top_frame, text="Dry Run", variable=self.builder_dry_run_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(top_frame, text="Offline", variable=self.builder_offline_var).pack(side=tk.LEFT, padx=5)
        
        
        ttk.Button(top_frame, text="Build & Run Command", command=self.run_pip_command_builder).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Check Dependencies", command=self.check_dependencies).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Package Info", command=self.fetch_package_info).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Suggest Packages", command=self.suggest_packages).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Usage Stats", command=self.show_usage_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Save Config", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Load Config", command=self.load_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Create Venv", command=self.create_virtual_env).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        
        
        self.builder_output = scrolledtext.ScrolledText(self.pip_builder_frame, height=15)
        self.builder_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def run_pip_command_builder(self):
        pkg = self.builder_pkg_entry.get().strip()
        if not pkg:
            messagebox.showwarning("Input Required", "Enter a package name.")
            return
        cmd = ["pip"]
        if self.builder_upgrade_var.get():
            cmd.append("install")
            cmd.append("--upgrade")
        elif self.builder_install_var.get():
            cmd.append("install")
        else:
            cmd.append("install")
        if self.builder_no_deps_var.get():
            cmd.append("--no-deps")
        if self.builder_user_var.get():
            cmd.append("--user")
        
        index_url = self.builder_index_entry.get().strip()
        if index_url:
            cmd.append("--index-url")
            cmd.append(index_url)
        cmd.append(pkg)
        self.builder_output.insert(tk.END, f"Running command: {' '.join(cmd)}\n")
        self.builder_output.see(tk.END)
        
        if self.builder_dry_run_var.get():
            self.builder_output.insert(tk.END, "[Dry Run] Command not executed.\n")
            self.builder_output.see(tk.END)
            self.add_to_command_history(cmd, "[Dry Run] Command not executed.\n")
            return
        threading.Thread(target=self.run_pip_command_builder_thread, args=(cmd,), daemon=True).start()
    
    def run_pip_command_builder_thread(self, cmd):
        try:
            process = subprocess.Popen(cmd,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            output = stdout + "\n" + stderr
            self.builder_output.insert(tk.END, output + "\n")
            diagnostics = self.get_error_diagnostics(output)
            if diagnostics:
                self.builder_output.insert(tk.END, "Diagnostics: " + diagnostics + "\n")
            self.builder_output.see(tk.END)
            self.add_to_command_history(cmd, output)
        except Exception as e:
            self.builder_output.insert(tk.END, f"Error: {e}\n")
            self.builder_output.see(tk.END)
    
    def check_dependencies(self):
        pkg = self.builder_pkg_entry.get().strip()
        if not pkg:
            messagebox.showwarning("Input Required", "Enter a package name.")
            return
        cmd = ["pip", "show", pkg]
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            output = stdout if stdout else stderr
            self.builder_output.insert(tk.END, f"Dependencies for {pkg}:\n{output}\n")
            self.builder_output.see(tk.END)
        except Exception as e:
            self.builder_output.insert(tk.END, f"Error checking dependencies: {e}\n")
            self.builder_output.see(tk.END)
    
    def fetch_package_info(self):
        pkg = self.builder_pkg_entry.get().strip()
        if not pkg:
            messagebox.showwarning("Input Required", "Enter a package name.")
            return
        if self.builder_offline_var.get():
            self.builder_output.insert(tk.END, "Offline Mode enabled. Cannot fetch package info.\n")
            self.builder_output.see(tk.END)
            return
        try:
            response = requests.get(f"https://pypi.org/pypi/{pkg}/json")
            if response.status_code == 200:
                data = response.json()
                info = data.get("info", {})
                summary = info.get("summary", "No description available")
                version = info.get("version", "Unknown")
                self.builder_output.insert(tk.END,
                    f"Package Info:\nName: {pkg}\nVersion: {version}\nSummary: {summary}\n\n")
            else:
                self.builder_output.insert(tk.END, f"Package {pkg} not found on PyPI.\n")
            self.builder_output.see(tk.END)
        except Exception as e:
            self.builder_output.insert(tk.END, f"Error fetching package info: {e}\n")
            self.builder_output.see(tk.END)
    
    def suggest_packages(self):
        partial = self.builder_pkg_entry.get().strip().lower()
        if not partial:
            messagebox.showwarning("Input Required", "Enter part of a package name for suggestions.")
            return
        
        popular = ["numpy", "pandas", "requests", "flask", "django", "scipy", "matplotlib", "tensorflow", "pytest", "beautifulsoup4"]
        suggestions = [pkg for pkg in popular if pkg.startswith(partial)]
        sugg_text = "Suggestions:\n" + "\n".join(suggestions) if suggestions else "No suggestions found."
        self.builder_output.insert(tk.END, sugg_text + "\n")
        self.builder_output.see(tk.END)
    
    def show_usage_stats(self):
        stats = {}
        for entry in getattr(self, 'command_history', []):
            cmd_str = entry["command"]
            stats[cmd_str] = stats.get(cmd_str, 0) + 1
        if stats:
            stats_text = "Usage Statistics:\n"
            for cmd, count in stats.items():
                stats_text += f"{cmd} : {count} times\n"
        else:
            stats_text = "No usage statistics available."
        self.builder_output.insert(tk.END, stats_text + "\n")
        self.builder_output.see(tk.END)
    
    def save_config(self):
        config = {
            "install": self.builder_install_var.get(),
            "upgrade": self.builder_upgrade_var.get(),
            "no_deps": self.builder_no_deps_var.get(),
            "user": self.builder_user_var.get(),
            "dry_run": self.builder_dry_run_var.get(),
            "offline": self.builder_offline_var.get(),
            "index_url": self.builder_index_entry.get().strip()
        }
        try:
            with open("pip_config.json", "w") as f:
                json.dump(config, f)
            self.builder_output.insert(tk.END, "Configuration saved.\n")
            self.builder_output.see(tk.END)
        except Exception as e:
            self.builder_output.insert(tk.END, f"Error saving config: {e}\n")
            self.builder_output.see(tk.END)
    
    def load_config(self):
        try:
            if not os.path.exists("pip_config.json"):
                self.builder_output.insert(tk.END, "No saved configuration found.\n")
                self.builder_output.see(tk.END)
                return
            with open("pip_config.json", "r") as f:
                config = json.load(f)
            self.builder_install_var.set(config.get("install", False))
            self.builder_upgrade_var.set(config.get("upgrade", False))
            self.builder_no_deps_var.set(config.get("no_deps", False))
            self.builder_user_var.set(config.get("user", False))
            self.builder_dry_run_var.set(config.get("dry_run", False))
            self.builder_offline_var.set(config.get("offline", False))
            self.builder_index_entry.delete(0, tk.END)
            self.builder_index_entry.insert(0, config.get("index_url", ""))
            self.builder_output.insert(tk.END, "Configuration loaded.\n")
            self.builder_output.see(tk.END)
        except Exception as e:
            self.builder_output.insert(tk.END, f"Error loading config: {e}\n")
            self.builder_output.see(tk.END)
    
    def create_virtual_env(self):
        venv_name = self.builder_venv_entry.get().strip()
        if not venv_name:
            messagebox.showwarning("Input Required", "Enter a virtual environment name.")
            return
        cmd = ["python", "-m", "venv", venv_name]
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            output = stdout + "\n" + stderr
            self.builder_output.insert(tk.END, f"Virtual environment creation output:\n{output}\n")
            self.builder_output.see(tk.END)
        except Exception as e:
            self.builder_output.insert(tk.END, f"Error creating virtual environment: {e}\n")
            self.builder_output.see(tk.END)
    
    def clear_output(self):
        self.builder_output.delete("1.0", tk.END)
    
    def get_error_diagnostics(self, output):
        diagnostics = []
        lower = output.lower()
        if "permission denied" in lower:
            diagnostics.append("Permission issue detected. Try using '--user' or run as administrator.")
        if "no matching distribution found" in lower or "could not find a version" in lower:
            diagnostics.append("Package not found. Verify package name or check its availability on PyPI.")
        return " ".join(diagnostics)
    
    def add_to_command_history(self, cmd, output):
        if not hasattr(self, 'command_history'):
            self.command_history = []
        self.command_history.append({"command": " ".join(cmd), "output": output})

    
    
    def create_placeholder_tab(self, title, message):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        ttk.Label(frame, text=message, foreground="red").pack(padx=10, pady=10)

def main():
    try:
        root = tk.Tk()
        app = AdvancedPipManager(root)
        root.mainloop()
    except Exception as e:
        print(f"Application stopped due to error: {e}")

if __name__ == "__main__":
    main()