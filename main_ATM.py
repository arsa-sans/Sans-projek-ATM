import tkinter as tk
from tkinter import ttk, messagebox
import json

class ATM:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM")
        self.root.geometry("300x300")
        self.root.resizable(False, False)
        
        # inisialisasi current_account
        self.current_account = None

        # memuat data akun dari file
        self.load_accounts()

        # memanggil widget GUI
        self.create_widgets()

    # fungsi memuat akun
    def load_accounts(self):
        try:
            with open("Data_Akun_ATM.json", "r") as f:
                raw_accounts = json.load(f)
                self.accounts = {
                    card: {
                        'name': data['name'],
                        'balance': int(data['balance'])
                    }
                    for card, data in raw_accounts.items()
                }
        except FileNotFoundError:
            self.accounts = {}
            self.save_accounts()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "File data rusak. Membuat file baru.")
            self.accounts = {}
            self.save_accounts()
    
    # fungsi save akun
    def save_accounts(self):
        try:
            with open("Data_Akun_ATM.json", "w") as f:
                json.dump(self.accounts, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")

    # membuat widgets
    def create_widgets(self):
        # frame untuk login
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(pady=20)
        
        tk.Label(self.login_frame, text="Silahkan Masukan Nomor Kartu Anda").pack(pady=5)
        self.card_entry = ttk.Entry(self.login_frame)
        self.card_entry.config(validate='key', validatecommand=(self.root.register(self.validate_card_number), '%P'))
        self.card_entry.pack(pady=5)

        # tombol login dan buat akun baru
        ttk.Button(self.login_frame, text='Login', command=self.login).pack(pady=10)
        ttk.Button(self.login_frame, text='Buat Akun Baru', command=self.show_create_account).pack(pady=20)

        # frame untuk operasi ATM
        self.atm_frame = ttk.Frame(self.root)

        # label informasi akun
        self.info_label = ttk.Label(self.atm_frame, font=('Arial', 14))
        self.info_label.pack(pady=10)

        # frame untuk operasi ATM
        frame_atm_operasi = ttk.Frame(self.atm_frame)
        frame_atm_operasi.pack(pady=10)

        ttk.Button(frame_atm_operasi, text='Tarik Tunai', command=self.show_withdraw).pack(side='left', padx=5)
        ttk.Button(frame_atm_operasi, text='Setor Tunai', command=self.show_deposit).pack(side='left', padx=5)
        ttk.Button(frame_atm_operasi, text='Keluar', command=self.logout).pack(side='left', padx=5)

        # frame untuk membuat akun baru
        self.create_account_frame = ttk.Frame(self.root)

        # memasukan username baru
        ttk.Label(self.create_account_frame, text='Nama :').pack(pady=5)
        self.name_entry = ttk.Entry(self.create_account_frame)
        self.name_entry.pack(pady=5)
        
        # membuat nomor kartu baru
        ttk.Label(self.create_account_frame, text='Nomor Kartu :').pack(pady=5)
        self.new_card = ttk.Entry(self.create_account_frame)
        self.new_card.config(validate='key',
                           validatecommand=(self.root.register(self.validate_card_number), '%P'))
        self.new_card.pack(pady=5)

        # memasukan saldo awal
        ttk.Label(self.create_account_frame, text='Saldo Awal :').pack(pady=5)
        self.initial_balance_entry = ttk.Entry(self.create_account_frame)
        self.initial_balance_entry.config(validate='key',
                                        validatecommand=(self.root.register(self.convert_to_digit), '%P'))
        self.initial_balance_entry.pack(pady=5)

        ttk.Button(self.create_account_frame, text='Buat Akun', command=self.create_account).pack(pady=5)
        ttk.Button(self.create_account_frame, text='Kembali', command=self.hide_create_account).pack(pady=5)

        # frame untuk operasi tarik tunai
        self.withdraw_frame = ttk.Frame(self.root)
        ttk.Label(self.withdraw_frame, text='Masukan Jumlah Penarikan :').pack(pady=5)
        self.withdraw_amount_entry = ttk.Entry(self.withdraw_frame)
        self.withdraw_amount_entry.config(validate='key',
                                        validatecommand=(self.root.register(self.convert_to_digit), '%P'))
        self.withdraw_amount_entry.pack(pady=5)
        ttk.Button(self.withdraw_frame, text='Tarik Tunai', command=self.withdraw).pack(pady=10)
        ttk.Button(self.withdraw_frame, text='Kembali', command=self.hide_withdraw).pack(pady=10)

        # frame untuk operasi setor tunai
        self.deposit_frame = ttk.Frame(self.root)
        ttk.Label(self.deposit_frame, text="Masukan Jumlah Setoran:").pack(pady=5)
        self.deposit_amount_entry = ttk.Entry(self.deposit_frame)
        self.deposit_amount_entry.config(validate='key',
                                       validatecommand=(self.root.register(self.convert_to_digit), '%P'))
        self.deposit_amount_entry.pack(pady=5)
        ttk.Button(self.deposit_frame, text="Setor Tunai", command=self.deposit).pack(pady=10)
        ttk.Button(self.deposit_frame, text="Kembali", command=self.hide_deposit).pack(pady=10)

    # info akun
    def update_info_account(self):
        if self.current_account:
            try:
                balance = int(self.current_account['balance'])
                self.info_label.config(text=f'Selamat datang, {self.current_account["name"]}!\nSaldo Anda: Rp. {balance:,}')
            except (ValueError, KeyError):
                messagebox.showerror("Error", "Format data saldo tidak valid")
                self.info_label.config(text='Error: Format saldo tidak valid')
        else:
            self.info_label.config(text='')

    # membatasi inputan nomor kartu
    def validate_card_number(self, new_value):
        if new_value == "":  # Mengizinkan field kosong (untuk backspace)
            return True
        if not new_value.isdigit():
            return False
        if len(new_value) > 6:
            return False
        return True
    
    # mengkonversi huruf jadi angka pada inputan harga
    def convert_to_digit(self, intejer):
        if intejer == "":  # Mengizinkan field kosong (untuk backspace)
            return True
        if not intejer.isdigit():
            return False
        return True

    # login
    def login(self):
        card_number = self.card_entry.get().strip()

        if not card_number:
            messagebox.showwarning('Peringatan!', 'Masukkan nomor kartu!')
            return

        if card_number in self.accounts:
            self.card_entry.delete(0, tk.END)
            self.current_account = self.accounts[card_number]
            self.login_frame.pack_forget()  # Sembunyikan frame login
            self.update_info_account()
            self.atm_frame.pack(pady=20)
        else:
            messagebox.showwarning('Peringatan!', 'Nomor kartu belum tersedia')

    # menampilkan frame akun baru
    def show_create_account(self):
        self.login_frame.pack_forget()  # Sembunyikan frame login
        self.create_account_frame.pack(pady=20)
    
    # menyembunyikan frame akun baru
    def hide_create_account(self):
        self.create_account_frame.pack_forget()
        self.login_frame.pack(pady=20)  # Tampilkan kembali frame login

    # fungsi membuat akun
    def create_account(self):
        name = self.name_entry.get().strip()
        card_number = self.new_card.get().strip()
        initial_balance = self.initial_balance_entry.get().strip()
        
        try:
            initial_balance = int(initial_balance)
            if initial_balance < 10000:
                messagebox.showwarning('Peringatan!', 'Saldo awal minimal Rp. 10.000')
                return
        except ValueError:
            messagebox.showwarning('Peringatan!', 'Saldo awal harus berupa angka')
            return
        
        if card_number in self.accounts:
            messagebox.showwarning('Peringatan!', 'Nomor kartu sudah ada')
        elif not name or not card_number:
            messagebox.showwarning('Peringatan!', 'Mohon lengkapi semua data')
        else:
            self.accounts[card_number] = {
                'name': name,
                'balance': initial_balance
            }
            self.save_accounts()
            messagebox.showinfo('Sukses', f"Akun baru telah dibuat!\nNama: {name}\nNomor Kartu: {card_number}\nSaldo Awal: Rp. {initial_balance:,}")
            self.name_entry.delete(0, tk.END)
            self.new_card.delete(0, tk.END)
            self.initial_balance_entry.delete(0, tk.END)
            self.hide_create_account()

    # menampilkan frame tarik tunai
    def show_withdraw(self):
        self.withdraw_frame.pack(pady=20)
        self.atm_frame.pack_forget()
    
    # menyembunyikan frame tarik tunai
    def hide_withdraw(self):
        self.withdraw_frame.pack_forget()
        self.atm_frame.pack(pady=20)

    # fungsi tarik tunai
    def withdraw(self):
        if not self.current_account:
            messagebox.showerror("Error", "Tidak ada akun yang aktif")
            self.hide_withdraw()
            return

        amount_str = self.withdraw_amount_entry.get().strip()
        
        try:
            amount = int(amount_str)
            current_balance = int(self.current_account['balance'])

            if amount <= 10000:
                messagebox.showwarning('Peringatan!', 'Jumlah penarikan harus lebih dari Rp. 10.000')
            elif current_balance >= amount:
                self.current_account['balance'] = current_balance - amount
                self.save_accounts()
                self.update_info_account()
                messagebox.showinfo('Sukses', f'Anda telah menarik tunai Rp. {amount:,}')
                self.hide_withdraw()
            else:
                messagebox.showwarning('Peringatan!', 'Saldo anda tidak mencukupi')
        except ValueError:
            messagebox.showwarning('Peringatan!', 'Masukan angka yang valid')
        finally:
            self.withdraw_amount_entry.delete(0, tk.END)

    # menampilkan frame deposit
    def show_deposit(self):
        self.deposit_frame.pack(pady=20)
        self.atm_frame.pack_forget()

    # menyembunyikan frame deposit
    def hide_deposit(self):
        self.deposit_frame.pack_forget()
        self.atm_frame.pack(pady=20)

    # fungsi deposit
    def deposit(self):
        if not self.current_account:
            messagebox.showerror("Error", "Tidak ada akun yang aktif")
            self.hide_deposit()
            return

        amount_str = self.deposit_amount_entry.get().strip()
        
        try:
            amount = int(amount_str)
            current_balance = int(self.current_account['balance'])
            if amount <= 10000:
                messagebox.showwarning('Peringatan!', 'Jumlah deposit harus lebih dari Rp. 10.000')
            else:
                self.current_account['balance'] = current_balance + amount
                self.save_accounts()
                self.update_info_account()
                messagebox.showinfo('Sukses', f'Anda telah menyetor tunai Rp. {amount:,}')
                self.hide_deposit()
        except ValueError:
            messagebox.showwarning('Peringatan!', 'Angka tidak valid')
        finally:
            self.deposit_amount_entry.delete(0, tk.END)

    # fungsi memeriksa tabungan
    def check_balance(self):
        self.update_info_account()

    # logout
    def logout(self):
        self.current_account = None
        self.atm_frame.pack_forget()
        self.login_frame.pack(pady=20)  # Tampilkan kembali frame login

def main():
    root = tk.Tk()
    app = ATM(root)
    root.mainloop()

if __name__ == "__main__":
    main()