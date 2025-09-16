import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import colorchooser
import tkinter.font as tkFont

# set the default color theme for the whole app
ctk.set_default_color_theme('autumn.json')
# appearance available system/light/dark
ctk.set_appearance_mode('system')
# define the app size
app_w, app_h = 1200, 800

class Watermarker_App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # app size
        self.geometry(f'{app_w}x{app_h}')
        self.title('Image Watermarking App')

        # text label
        self.textLabel = ctk.CTkLabel(
            self,
            text='Watermark text: '
        )
        self.textLabel.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky='ew'
        )
        # Name Entry Field
        self.textEntry_var = tk.StringVar()
        self.textEntry = ctk.CTkEntry(
            self,
            placeholder_text="Enter text"
        )
        self.textEntry.grid(
            row=0,
            column=1,
            columnspan=5,
            padx=20,
            pady=20,
            sticky="ew"
        )


        # font types
        self.fontLabel = ctk.CTkLabel(
            self,
            text='Font: '
        )
        self.fontLabel.grid(
            row=1,
            column=0,
            padx=20,
            pady=20,
            sticky='ew'
        )
        fonts = sorted(tkFont.families())  # get system fonts
        # font dropdown
        self.font_var = tk.StringVar(value="Arial")  # default font
        self.font_menu = ctk.CTkOptionMenu(
            self,
            values=fonts,
            variable=self.font_var,
            command=self.update_font  # called when user selects a font
        )
        self.font_menu.grid(
            row=3,
            column=1,
            padx=20,
            pady=20,
            sticky="ew"
        )


        # font_size
        self.font_sizeLabel = ctk.CTkLabel(
             self,
             text='Choose font size: '
        )
        self.font_sizeLabel.grid(
            row=2,
            column=0,
            padx=20,
            pady=20,
            sticky='ew'
        )
        self.font_size_spinbox = tk.Spinbox(
            self,
            from_=5,
            to=30,
            width=5,
            command=self.update_font
            )
        self.font_size_spinbox.grid(
            row=2,
            column=1,
            padx=20,
            pady=20,
            sticky='ew'
        )

        # user to choose a font color
        self.color_button_var = tk.StringVar(value="white")  # default font
        self.color_buttonLabel = ctk.CTkLabel(
            self,
            text='Choose font color: ',
            variable=self.color_button_var
        )
        self.color_buttonLabel.grid(
            row=3,
            column=0,
            padx=20,
            pady=20,
            sticky='ew'
        )
        self.color_button = tk.Button(
            self,
            text='Select',
            command = self.update_color
        )
        self.color_button.grid(
            row=3,
            column=1,
            padx=20,
            pady=20,
            sticky='ew'
        )

    # update font according to the user input
    def update_font(self, choice=None):
        font_name = self.font_var.get()
        font_size = int(self.font_size_spinbox.get())
        self.textEntry.config(font=(font_name, font_size))

    # update font color according to the user input
    def update_color(self):
        color_code = colorchooser.askcolor(title='Choose font color')
        if color_code[1]:  # hex colour
            self.color_button.config(
                            text=color_code[1],
                            bg=color_code[1],
                            fg='black' if color_code[1].lower() != "#ffffff" else "black"
                            )





if __name__ == '__main__':
    app = Watermarker_App()
    app.mainloop()