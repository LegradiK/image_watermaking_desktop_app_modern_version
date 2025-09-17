import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import colorchooser
import tkinter.font as tkFont
from PIL import ImageColor


# set the default color theme for the whole app
ctk.set_default_color_theme('autumn.json')
# appearance available system/light/dark
ctk.set_appearance_mode('dark')
# define the app size
app_w, app_h = 1300, 800

class Watermarker_App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # app size
        self.geometry(f'{app_w}x{app_h}')
        self.title('Image Watermarking App')

        # picture frame
        self.picture_frame = ctk.CTkFrame(
            master=self,
            width=900,
            height=800,
            corner_radius=5,
            border_width=2
        )
        self.picture_frame.pack(pady=10, padx=5, fill='y', side='left')




        # frame for control panel
        self.control_panel_frame = ctk.CTkFrame(
            master=self,
            width=200,
            height=800,
            corner_radius=5,
            border_width=2
        )
        self.control_panel_frame.pack(pady=10, padx=5, fill='y', side='right')

        # text label
        self.textLabel = ctk.CTkLabel(
            self.control_panel_frame,
            text='Watermark text: '
        )
        self.textLabel.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky='ew'
        )
        # add frame for text box
        self.text_frame = ctk.CTkScrollableFrame(
            self.control_panel_frame,
            orientation='horizontal',
            width=180,
            height=50,
            label_text='Enter text'
            )
        self.text_frame.grid(row=0, column=1, pady=20, padx=20)

        # Entry text box
        self.textEntry_var = tk.StringVar()
        self.textEntry = tk.Text(
            self.text_frame
        )
        self.textEntry.grid(
            row=0, column=0,
            sticky="ew"
        )


        # font types
        self.fontLabel = ctk.CTkLabel(
            self.control_panel_frame,
            text='Font style: '
        )
        self.fontLabel.grid(
            row=3,
            column=0,
            padx=20,
            pady=20,
            sticky='ew'
        )
        fonts = sorted(tkFont.families())
        # font dropdown
        self.font_var = tk.StringVar(value="Arial")  # default font
        self.font_menu = ctk.CTkOptionMenu(
            self.control_panel_frame,
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
        self.font_size_var = tk.IntVar(value=10)
        self.font_sizeLabel = ctk.CTkLabel(
             self.control_panel_frame,
             text='Font size: '
        )
        self.font_sizeLabel.grid(
            row=4,
            column=0,
            padx=20,
            pady=20,
            sticky='ew'
        )
        self.font_size_var.trace_add("write", lambda *args: self.update_font())
        self.font_size_spinbox = tk.Spinbox(
            self.control_panel_frame,
            from_=5,
            to=30,
            width=5,
            textvariable=self.font_size_var
            )
        self.font_size_spinbox.grid(
            row=4,
            column=1,
            padx=20,
            pady=20,
            sticky='ew'
        )

        # user to choose a font color
        self.font_color_var = tk.StringVar(value="black")  # default font
        self.font_colorLabel = ctk.CTkLabel(
            self.control_panel_frame,
            text='Font color: '
        )
        self.font_colorLabel.grid(
            row=5,
            column=0,
            padx=20,
            pady=20,
            sticky='ew'
        )
        self.font_color = tk.Button(
            self.control_panel_frame,
            text='Select',
            command = self.update_color
        )
        self.font_color.grid(
            row=5,
            column=1,
            padx=20,
            pady=20,
            sticky='ew'
        )

        # apply transparency to font
        self.font_transparency_slider_var = tk.IntVar(value=100)  # default transparency
        self.font_transparency_sliderLabel = ctk.CTkLabel(
            self.control_panel_frame,
            text='Transparency (0-100%): '
        )
        self.font_transparency_sliderLabel.grid(
            row=6,
            column=0,
            padx=20,
            pady=20,
            sticky='ew'
        )
        self.font_transparency_slider = ctk.CTkSlider(
            self.control_panel_frame,
            from_=0,
            to=100,
            command=self.update_transparency
        )
        self.font_transparency_slider.grid(
            row=6,
            column=1,
            padx=20,
            pady=20,
            sticky='ew'
        )

    # update font according to the user input
    def update_font(self):
        """update font type and size according to the user's choice"""
        font_type = self.font_var.get() if hasattr(self, "font_var") else "Arial"
        try:
            font_size = int(self.font_size_var.get())
        except (ValueError, TypeError):
            font_size = 12 # detault
        font_color = self.font_color_var.get() if hasattr(self, "font_color_var") else "black"
        self.textEntry.config(font=(font_type, font_size), fg=font_color)

    # update font color according to the user input
    def update_color(self):
        """Update font color according to the user's choice"""
        color_code = colorchooser.askcolor(title='Choose font color')
        if color_code[1]:  # hex colour
            self.font_color_var.set(color_code[1])
            self.font_color.config(
                            text=color_code[1],
                            bg=color_code[1],
                            fg='black' if color_code[1].lower() != "#ffffff" else "black"
                            )
            self.update_font()

    def update_transparency(self, value):
        self.font_transparency_slider_var = int(float(value) * 255 / 100)




if __name__ == '__main__':
    app = Watermarker_App()
    app.mainloop()