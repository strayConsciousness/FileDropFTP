import tkinter as tk
from tkinter import messagebox
import ftplib as ftp_client
# from ftplib import FTP

class FTPClient:
    # this is the main function that executes first
    def __init__(self, host, username, password, port=21):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ftp = ftp_client.FTP()

    # establishing connection using ftp.connect
    def connect(self):
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.username, self.password)
        print("Connected to FTP server.")

    # listing files using dir command
    def list_files(self):
        # self.ftp.dir()
        if not self.ftp:
            raise ValueError("FTP connection not established.")

        try:
            # nlst() for printing multiple files
            files = self.ftp.nlst()
            return files
        except Exception as e:
            raise RuntimeError(f"Error listing files: {str(e)}")

    # for downloading files to the main code location
    def download_file(self, remote_path, local_path):
        with open(local_path, 'wb') as local_file:
            self.ftp.retrbinary('RETR ' + remote_path, local_file.write)
        print(f"Downloaded {remote_path} to {local_path}")

    # def upload_file(self, local_path, remote_path):
    #     with open(local_path, 'rb') as local_file:
    #         self.ftp.storbinary('STOR ' + remote_path, local_file)
    #     print(f"Uploaded {local_path} to {remote_path}")
    #
    # def delete_file(self, remote_path):
    #     self.ftp.delete(remote_path)
    #     print(f"Deleted {remote_path}")

    # disconnecting form the server
    def disconnect(self):
        try:
            self.ftp.quit()
            print("Disconnected from FTP server.")
        except EOFError:
            print("Already disconnected from FTP server.")

class FTPClientGUI:
    def __init__(self, master):
        # self.host = host
        # self.port = port
        # self.username = username
        # self.password = password
        # self.ftp = ftplib.FTP()

        self.master = master
        self.master.title("FileDrop FTP")

        # Software Title
        self.label_title = tk.Label(master, text="FileDrop FTP Client", font=("Montserrat", 24, "bold"), fg="blue", bg="#E4E9DF")
        self.label_title.place(x=190,y=5)

        #  DATA FOR MAKING CONNECTION
        self.label_host = tk.Label(master, text="Host:", bg="#E4E9DF", font=("Roboto", 11))
        self.label_host.place(x=50, y=70)
        self.entry_host = tk.Entry(master)
        self.entry_host.place(x=150, y=70)

        self.label_username = tk.Label(master, text="Username:", bg="#E4E9DF", font=("Roboto", 11))
        self.label_username.place(x=50, y=140)
        self.entry_username = tk.Entry(master)
        self.entry_username.place(x=150, y=140)

        self.label_password = tk.Label(master, text="Password:", bg="#E4E9DF", font=("Roboto", 11))
        self.label_password.place(x=50, y=210)
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.place(x=150, y=210)

        self.label_port = tk.Label(master, text="Port:", bg="#E4E9DF", font=("Roboto", 11))
        self.label_port.place(x=50, y=280)
        self.entry_port = tk.Entry(master)
        self.entry_port.place(x=150, y=280)

        self.button_connect = tk.Button(master, text="Connect", command=self.connect, bg="#E4E9DF", font=("Montserrat", 11))
        self.button_connect.place(x=125, y=350)

        #  DATA FOR DOWNLOADING FILES
        self.label_remote_path = tk.Label(master, text="Remote Path:", bg="#E4E9DF", font=("Roboto", 11))
        self.label_remote_path.place(x=350, y=70)
        self.entry_remote_path = tk.Entry(master)
        self.entry_remote_path.place(x=470, y=70)

        self.label_local_path = tk.Label(master, text="Local Path:", bg="#E4E9DF", font=("Roboto", 11))
        self.label_local_path.place(x=350, y=140)
        self.entry_local_path = tk.Entry(master)
        self.entry_local_path.place(x=470, y=140)

        self.button_download = tk.Button(master, text="Download Files", command=self.download_file, bg="#E4E9DF", font=("Montserrat", 11))
        self.button_download.place(x=410, y=210)

        #  LISTING FILES IN THE CURRENT FTP DIRECTORY
        self.button_list_files = tk.Button(master, text="List Files", command=self.list_files, bg="#E4E9DF", font=("Montserrat", 11))
        self.button_list_files.place(x=425, y=280)

        #  DISCONNECTING
        self.button_disconnect = tk.Button(master, text="Disconnect", command=self.disconnect, bg="red", fg="white", font=("Montserrat", 11, "bold"))
        self.button_disconnect.place(x=420, y=350)

        # Team Details
        self.label_title = tk.Label(master, text="22BCS17134 [RAJAT] \n 22BCS17121 [JASWANTH]", font=("Montserrat", 8, "bold"), fg="red",bg="#E4E9DF")
        # self.label_title = tk.Label(master, text="22BCS17121 JASWANTH", font=("Montserrat", 8, "bold"), fg="red", bg="#E4E9DF")
        self.label_title.place(x=250, y=430)

    def connect(self):
        host = self.entry_host.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        port = self.entry_port.get()

        try:
            port = int(port)
            self.ftp_client = FTPClient(host, username, password, port)
            self.ftp_client.connect()
            messagebox.showinfo("FTP Client", "Connected to FTP server.")
        except ValueError:
            messagebox.showerror("FTP Client", "Invalid port number.")
        except Exception as e:
            messagebox.showerror("FTP Client", f"Error: {str(e)}")

    def download_file(self):
        if not self.ftp_client:
            messagebox.showwarning("FTP Client", "Not connected to FTP server.")
            return

        # download operation
        try:
            remote_path = self.entry_remote_path.get().strip()
            local_path = self.entry_local_path.get().strip()

            with open(local_path, 'wb') as f:
                self.ftp_client.ftp.retrbinary('RETR ' + remote_path, f.write)

            messagebox.showinfo("FTP Client", "File downloaded successfully.")

        except Exception as e:
            messagebox.showerror("FTP Client", f"Error downloading file: {str(e)}")

    def list_files(self):
        if not self.ftp_client:
            messagebox.showwarning("FTP Client", "Not connected to FTP server.")
            return []

        try:
            files = [filename.strip('\ufeff') for filename in self.ftp_client.ftp.nlst()]
            messagebox.showinfo("FTP Client", f"Files in the current directory:\n{files}")
            return files
        except Exception as e:
            messagebox.showerror("FTP Client", f"Error listing files: {str(e)}")
            return []

    def disconnect(self):
        if self.ftp_client and self.ftp_client.ftp:
            try:
                self.ftp_client.disconnect()
                messagebox.showinfo("FTP Client", "Disconnected from FTP server.")
            except EOFError:
                messagebox.showwarning("FTP Client", "FTP connection already closed.")
        else:
            messagebox.showwarning("FTP Client", "Not connected to FTP server.")

def main():

    root = tk.Tk()
    root.geometry("670x470")
    root.configure(bg="#E4E9DF")
    app = FTPClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
