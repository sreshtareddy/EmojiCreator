import streamlit as st
import pandas as pd
import os
import time
import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import os
import numpy as np
import cv2
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras.optimizers import Adam
from keras.layers import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from tkinter import messagebox as tkMessageBox
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():

	st.title("Welcome to Emoji World!")
	st.image("college.jpg")
	st.sidebar.subheader("Department Of Computer Science")
	st.sidebar.image("logo.png")
	menu = ["Home","Login","SignUp"]

	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Emojify - Converts Realtime face expressions to Emoji/Avatar")
		st.subheader("")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))
				st.write("Click here to run the Application")
				if st.button("Start Application"):


					emotion_model = Sequential()
					emotion_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
					emotion_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
					emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
					emotion_model.add(Dropout(0.25))
					emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
					emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
					emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
					emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
					emotion_model.add(Dropout(0.25))
					emotion_model.add(Flatten())
					emotion_model.add(Dense(1024, activation='relu'))
					emotion_model.add(Dropout(0.5))
					emotion_model.add(Dense(7, activation='softmax'))
					emotion_model.load_weights('model.h5')
					cv2.ocl.setUseOpenCL(False)
					emotion_dict = {0: "   Angry   ", 1: "Disgusted", 2: "  Fearful  ", 3: "   Happy   ",
									4: "  Natural  ",
									5: "    Sad    ", 6: "Surprised"}
					emoji_dist = {0: "emojis/angry.png", 1: "emojis/disgusted.png", 2: "emojis/fearful.png",
								  3: "emojis/happy.png",
								  4: "emojis/neutral.png", 5: "emojis/happy1.png", 6: "emojis/surprised.png"}
					global last_frame1
					last_frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
					global cap1
					show_text = [0]
					
					def close_all_apps():
						#command = os.popen('taskkill /f /IM chrome.exe')
						os.system('cmd /c "taskkill /f /IM chrome.exe"')
						os.system('cmd /c "taskkill /f /IM cmd.exe"')
						#pyautogui.hotkey('ctrl','c')
						#command = os.popen('taskkill /f /IM cmd.exe')
						time.sleep(1)
						exit(0)

					def helloCallBack():
						result = tkMessageBox.askyesno("Hello Python", "Are you sure you want to quit?")
						if result:
							close_all_apps()

					def show_vid():
						cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)

						if not cap1.isOpened():
							print("cant open the camera1")
						flag1, frame1 = cap1.read()
						frame1 = cv2.resize(frame1, (500, 370))
						bounding_box = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
						gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
						num_faces = bounding_box.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)
						for (x, y, w, h) in num_faces:
							cv2.rectangle(frame1, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
							roi_gray_frame = gray_frame[y:y + h, x:x + w]
							cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
							prediction = emotion_model.predict(cropped_img)
							maxindex = int(np.argmax(prediction))
							cv2.putText(frame1, emotion_dict[maxindex], (x + 20, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
										(255, 255, 255), 2,
										cv2.LINE_AA)
							show_text[0] = maxindex

						if flag1 is None:
							print("Major error!")
						elif flag1:
							global last_frame1
							last_frame1 = frame1.copy()
							pic = cv2.cvtColor(last_frame1, cv2.COLOR_BGR2RGB)
							img = Image.fromarray(pic)
							imgtk = ImageTk.PhotoImage(image=img)
							lmain.imgtk = imgtk
							lmain.configure(image=imgtk)
							lmain.after(300, show_vid)
						if cv2.waitKey(1) & 0xFF == ord('q'):
							exit()

					def show_vid2():
						frame2 = cv2.imread(emoji_dist[show_text[0]])
						pic2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
						img2 = Image.fromarray(pic2)
						imgtk2 = ImageTk.PhotoImage(image=img2)
						lmain2.imgtk2 = imgtk2
						lmain3.configure(text=emotion_dict[show_text[0]], font=('arial', 45, 'bold'))

						lmain2.configure(image=imgtk2, width=500, height=370)
						lmain2.after(500, show_vid2)

					class FullScreenApp(object):
						def __init__(self, master, **kwargs):
							self.master = master
							pad = 3
							self._geom = '200x200+0+0'
							master.geometry("{0}x{1}+0+0".format(
								master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
							master.bind('<Escape>', self.toggle_geom)

						def toggle_geom(self, event):
							geom = self.master.winfo_geometry()
							print(geom, self._geom)
							self.master.geometry(self._geom)
							self._geom = geom

					if __name__ == '__main__':
						root = tk.Tk()
						img = ImageTk.PhotoImage(Image.open("Logo.png"))
						heading = Label(root, image=img, bg='black', width=1, height=1)

						heading.pack()
						heading2 = Label(root, text="Welcome to Emoji World!", pady=50,
										 font=('times new roman', 55, 'bold'), bg='#0f0f0f',
										 fg='#f5f7f0')

						heading2.pack()
						lmain = tk.Label(master=root, padx=50, bd=10)
						lmain2 = tk.Label(master=root, bd=10)
						lmain3 = tk.Label(master=root, bd=10, fg="#7f5be3", bg='#0f0f0f')
						lmain.pack(side=LEFT)
						lmain.place(x=160, y=280)
						lmain3.pack()
						lmain3.place(x=940, y=180)
						lmain2.pack(side=RIGHT)
						lmain2.place(x=840, y=280)

						root.title("Face to Emoji")
						app = FullScreenApp(root)
						root['bg'] = '#0f0f0f'
						exitbutton = Button(root, text='QUIT', command=helloCallBack, fg='red', height=1, width=10,
											font=('times new roman', 20, 'bold')).place(x=685,
																						y=730)

						show_vid()
						show_vid2()
						root.mainloop()



			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()