import tkinter as tk
import socket
import threading
import sys


class ChatApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat")

        self.bg_color = "#3A3A3A"
        self.text_color = "#EEEEEE"
        self.button_color = "#4CAF50"
        self.button_hover_color = "#45a049"

        self.label_font = ("Helvetica", 12)
        self.entry_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 12, "bold")
        self.text_font = ("Helvetica", 12)

        self.root.configure(bg=self.bg_color)

        self.label_ip = tk.Label(root, text="IP:", font=self.label_font, bg=self.bg_color, fg=self.text_color)
        self.label_ip.grid(row=0, column=0, padx=10, pady=5)
        self.entry_ip = tk.Entry(root, font=self.entry_font)
        self.entry_ip.grid(row=0, column=1, padx=10, pady=5)

        self.label_port = tk.Label(root, text="Port:", font=self.label_font, bg=self.bg_color, fg=self.text_color)
        self.label_port.grid(row=1, column=0, padx=10, pady=5)
        self.entry_port = tk.Entry(root, font=self.entry_font)
        self.entry_port.grid(row=1, column=1, padx=10, pady=5)

        self.label_nickname = tk.Label(root, text="Nickname:", font=self.label_font, bg=self.bg_color, fg=self.text_color)
        self.label_nickname.grid(row=2, column=0, padx=10, pady=5)
        self.entry_nickname = tk.Entry(root, font=self.entry_font)
        self.entry_nickname.grid(row=2, column=1, padx=10, pady=5)

        self.button_connect = tk.Button(root, text="Connect", font=self.button_font, bg=self.button_color, fg="white", command=self.connect)
        self.button_connect.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.text_messages = tk.Text(root, font=self.text_font, bg="#737373", fg=self.text_color, wrap="word")
        self.text_messages.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.entry_message = tk.Entry(root, font=self.entry_font)
        self.entry_message.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.entry_message.insert(0, "Digite sua mensagem aqui...")
        self.entry_message.bind("<FocusIn>", self.clear_placeholder)

        self.button_send = tk.Button(root, text="Send", font=self.button_font, bg=self.button_color, fg="white", command=self.send_message)
        self.button_send.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.tcp_connection = None
        self.receive_thread = None

    def connect(self):
        ip = self.entry_ip.get()
        port = self.entry_port.get()
        nickname = self.entry_nickname.get()

        if not ip or not port or not nickname:
            self.display_message("Insira o IP, a porta e o nickname.")
            return

        try:
            self.tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_connection.connect((ip, int(port)))
            self.tcp_connection.send(nickname.encode())

            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()

            self.display_message("Conectado no servidor.")
        except Exception as e:
            self.display_message(f"Erro conectando no servidor: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.tcp_connection.recv(1024).decode()
                if not message:
                    break
                self.display_message(message)
            except Exception as e:
                break

    def send_message(self):
        if not self.tcp_connection:
            self.display_message("Not connected to server.")
            return

        message = self.entry_message.get()
        if not message:
            return

        try:
            self.tcp_connection.send(message.encode())
            self.display_message(f"You: {message}")
            self.entry_message.delete(0, tk.END)
        except Exception as e:
            self.display_message(f"Error sending message: {e}")

    def display_message(self, message):
        self.text_messages.insert(tk.END, message + "\n")
        self.text_messages.see(tk.END)

    def clear_placeholder(self, event):
        if self.entry_message.get() == "Digite sua mensagem aqui...":
            self.entry_message.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()
