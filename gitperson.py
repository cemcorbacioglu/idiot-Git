import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def fetch_github_info(event=None):
    username = entry_username.get()
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        name = data.get('name', 'Not available')
        public_repos = data.get('public_repos', 'Not available')
        followers = data.get('followers', 'Not available')
        following = data.get('following', 'Not available')

        avatar_url = data.get('avatar_url', '')
        try:
            response = requests.get(avatar_url, stream=True)  # Add stream=True
            response.raw.decode_content = True
            avatar_image = Image.open(response.raw)
            avatar_image.thumbnail((80, 80))
            avatar_photo = ImageTk.PhotoImage(avatar_image)
            label_avatar.config(image=avatar_photo)
            label_avatar.image = avatar_photo
        except Exception as e:
            print("Error loading image:", e)

    else:
        error_message = data.get('message', 'An error occurred')
        name = public_repos = followers = following = error_message

    label_name["text"] = f"Name: {name}"
    label_repos["text"] = f"Public Repositories: {public_repos}"
    label_followers["text"] = f"Followers: {followers}"
    label_following["text"] = f"Following: {following}"


root = tk.Tk()
root.title("GitHub User Info")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

style.configure(".", font=("Arial", 12))
style.configure("TLabel", foreground="#e0e0e0", background="#222222")
style.configure("TEntry", fieldbackground="#303030", foreground="#e0e0e0")
style.configure("TButton", background="#333333", foreground="#e0e0e0")
style.configure("TFrame", background="#222222")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0)

label_username = ttk.Label(frame, text="GitHub Username:")
label_username.grid(row=0, column=0, sticky=tk.W)

entry_username = ttk.Entry(frame)
entry_username.grid(row=0, column=1, sticky=tk.W)

button_submit = ttk.Button(frame, text="Fetch Info", command=fetch_github_info)
button_submit.grid(row=0, column=2, padx=(10, 0))

label_avatar = tk.Label(frame, background="#222222")  # Use tk.Label instead of ttk.Label
label_avatar.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky=tk.W)

label_name = ttk.Label(frame, text="")
label_name.grid(row=2, column=0, columnspan=3, sticky=tk.W)

label_repos = ttk.Label(frame, text="")
label_repos.grid(row=3, column=0, columnspan=3, sticky=tk.W)

label_followers = ttk.Label(frame, text="")
label_followers.grid(row=4, column=0, columnspan=3, sticky=tk.W)

label_following = ttk.Label(frame, text="")
label_following.grid(row=5, column=0, columnspan=3, sticky=tk.W)

entry_username.focus()
root.bind('<Return>', fetch_github_info)

root.configure(bg="#222222")
root.mainloop()
