import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import colorchooser
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageColor
import matplotlib.font_manager as fm



# set the default color theme for the whole app
ctk.set_default_color_theme('autumn.json')
# appearance available system/light/dark
ctk.set_appearance_mode('dark')
# define the app size
app_w, app_h = 1360, 800
pic_frame_w, pic_frame_h = 900, 800

class Watermarker_App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # app size
        self.geometry(f'{app_w}x{app_h}')
        self.title('Image Watermarking App')

        # picture frame
        self.picture_frame = ctk.CTkFrame(
            master=self,
            width=pic_frame_w,
            height=pic_frame_h,
            corner_radius=5,
            border_width=2
        )
        self.picture_frame.pack(pady=10, padx=5, fill='y', side='left')

        # stop shrinking to fit contents
        self.picture_frame.pack_propagate(False)

        # get a correct color depending on the setting
        frame_color = self.picture_frame.cget("fg_color")
        # get a screen mode
        screen_mode = ctk.get_appearance_mode().lower()
        screen_color = ''
        # determine a valid color string
        if isinstance(frame_color, list):
            screen_color = frame_color[0] if screen_mode == "light" else frame_color[1]
        else:
            screen_color = frame_color  # already a single color string
        # setting a canvas
        self.pic_canvas = tk.Canvas(
            self.picture_frame,
            width=pic_frame_w,
            height=pic_frame_h,
            highlightthickness=0,             # remove border
            bd=0,                             # no 3D border
            bg=screen_color  # match CTkFrame background
        )
        self.pic_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.upload_button = ctk.CTkButton(
            self.picture_frame,
            text='Upload picture',
            height=100,
            width=100,
            font=('Ariel',24),
            hover=True,
            hover_color='grey',
            corner_radius=10,
            command=self.upload_pic
        )
        # show a button at the centre of pic frame
        self.upload_button.place(relx=0.5, rely=0.5, anchor="center")


        # frame for control panel
        self.control_panel_frame = ctk.CTkFrame(
            master=self,
            width=200,
            height=800,
            corner_radius=5,
            border_width=2
        )
        self.control_panel_frame.pack(pady=10, padx=5, fill='y', side='right')

        # stop shrinking to fit contents
        self.control_panel_frame.pack_propagate(False)

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
            height=50
            )
        self.text_frame.grid(row=0, column=1, pady=20, padx=20)

        # Entry text box
        self.textEntry = ctk.CTkTextbox(
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
        self.font_var = tk.StringVar(value="DejaVu Serif")  # default font
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
             text='Font size (in %): '
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
        self.font_color_var = tk.StringVar(value="white")  # default font
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
        self.font_color_button = tk.Button(
            self.control_panel_frame,
            text='Select',
            command = self.update_color
        )
        self.font_color_button.grid(
            row=5,
            column=1,
            padx=20,
            pady=20,
            sticky='ew'
        )

        # apply transparency to font
        self.font_transparency_slider_var = 255  # default transparency
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
            padx=5,
            pady=5,
            sticky='ew'
        )

        self.apply_buttonButton = ctk.CTkButton(
            self.control_panel_frame,
            text='Apply',
            command=self.waterMarker
        )
        self.apply_buttonButton.grid(
            row=7,
            column=1,
            padx=5,
            pady=5,
            sticky='ew'
        )

    # Upload pic
    def upload_pic(self):
        """ Upload a picture from system"""
        fileTypes = [("Image Files", "*.jpg *.jpeg *.png")]
        path = tk.filedialog.askopenfilename(filetypes=fileTypes)
        if len(path):
            self.image_path = path
            self.img = Image.open(path)
            self.img_w, self.img_h = self.img.size
            if self.img_w > pic_frame_w and self.img_h> pic_frame_h:
                self.img.thumbnail((pic_frame_w-20, pic_frame_h-20), Image.LANCZOS)
            pic = ImageTk.PhotoImage(self.img)

            # hide the upload button
            self.upload_button.place_forget()

            self.pic_canvas.delete('all')
            self.pic_canvas.create_image(0, 0, image=pic, anchor='nw')
            self.pic_canvas.image = pic
        else:
            print('No file is selected')

    def waterMarker(self):
        """pulling all the info from apply_watermark, then display watermarked image"""

        watermarked_pic = self.apply_watermark()
        if watermarked_pic:
            display_img = watermarked_pic.copy()
            display_img.thumbnail((pic_frame_w, pic_frame_h), Image.LANCZOS)

            tk_img = ImageTk.PhotoImage(display_img)
            self.pic_canvas.delete('all')
            self.pic_canvas.create_image(0, 0, image=tk_img, anchor='nw')
            self.pic_canvas.image = tk_img



    def apply_watermark(self):
        """ getting all the input about how a user wants to watermark a pic"""
        # get image_path
        if not self.image_path:
            messagebox.showwarning('No image','Please upload an image')
            return

        # get user text input
        text = self.textEntry.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning('No text','Please type watermarking text')
            return

        # get font_size input
        try:
            font_size_percent = int(self.font_size_var.get())
        except (ValueError, TypeError, TclError):
            font_size_percent = 10  # default %

        font_size = int(min(self.img_w, self.img_h) * font_size_percent / 100)

        font_style = self.font_var.get()
        font_color = self.font_color_var.get()
        font_transparency = self.font_transparency_slider_var

        base = self.img.convert('RGBA')
        # create another layer where watermark will be on
        text_layer = Image.new('RGBA', self.img.size, (255, 255, 255, 0))
        # deciding the test_layer and font details
        draw = ImageDraw.Draw(text_layer)

        font_files = fm.findSystemFonts()
        font_lookup = {fm.FontProperties(fname=f).get_name(): f for f in font_files}

        font_path = font_lookup.get(font_style)  # from your OptionMenu
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (base.width - text_w) // 2
        y = (base.height - text_h) // 2

        # Decide position: centre of the image
        x = base.width // 2
        y = base.height // 2

        # Apply transparency to colour
        r, g, b = ImageColor.getrgb(font_color)
        draw.text((x, y), text, font=font, fill=(r, g, b, font_transparency))

        # Merge layers
        combined = Image.alpha_composite(base, text_layer)

        return combined

    # update font according to the user input
    def update_font(self, value=None):
        """update font type and size according to the user's choice"""
        font_type = self.font_var.get() if hasattr(self, "font_var") else "Arial"
        try:
            font_size = int(self.font_size_var.get())
        except (ValueError, TypeError, TclError):
            font_size = 12 # detault
        font_color = self.font_color_var.get() if hasattr(self, "font_color_var") else "white"
        self.textEntry.configure(font=(font_type, font_size), text_color=font_color)

    # update font color according to the user input
    def update_color(self):
        """Update font color according to the user's choice"""
        color_code = colorchooser.askcolor(title='Choose font color')
        if color_code[1]:  # hex colour
            self.font_color_var.set(color_code[1])
            self.font_color_button.configure(
                            text=color_code[1],
                            bg=color_code[1],
                            fg='black' if color_code[1].lower() != "#ffffff" else "black"
                            )
            self.update_font()

    def update_transparency(self, value):
        """get a user input for the transparency of text"""
        self.font_transparency_slider_var = int(float(value) * 255 / 100)





if __name__ == '__main__':
    app = Watermarker_App()
    app.mainloop()