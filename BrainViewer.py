import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from glob import glob

class NiftiViewer:
    def __init__(self, master, file_list, speed):
        self.master = master
        self.file_list = file_list
        self.speed = speed
        self.index = 0  # subject index
        self.slice_indices = {}
        self.animating = {}  # keep track of which orientation is animating

        # Load first subject
        self.load_subject(self.file_list[self.index])

        # GUI Layout
        self.master.title("NIfTI Brain Viewer")

        self.label = tk.Label(master, text=f"Subject: {self.subject_number}", font=("Arial", 14))
        self.label.pack()

        nav_frame = tk.Frame(master)
        nav_frame.pack(pady=5)

        prev_btn = tk.Button(nav_frame, text="Previous Subject", command=self.prev_subject)
        prev_btn.grid(row=0, column=0, padx=5)

        next_btn = tk.Button(nav_frame, text="Next Subject", command=self.next_subject)
        next_btn.grid(row=0, column=1, padx=5)
        frame = tk.Frame(master)
        frame.pack()

        self.figures = {}
        self.canvases = {}
        self.axes = {}
        self.buttons = {}

        for i, orientation in enumerate(['sagittal', 'coronal', 'axial']):
            subframe = tk.Frame(frame)
            subframe.grid(row=0, column=i, padx=5, pady=5)

            fig, ax = plt.subplots(figsize=(2, 2), dpi=100)
            fig.subplots_adjust(left=0, right=1, top=0.8, bottom=0)

            canvas = FigureCanvasTkAgg(fig, master=subframe)
            canvas.get_tk_widget().pack()

            self.entry = tk.Entry(nav_frame, width=10)
            self.entry.grid(row=0, column=2, padx=5)
            go_btn = tk.Button(nav_frame, text="Go", command=self.go_to_subject)
            go_btn.grid(row=0, column=3, padx=5)

            btn_frame = tk.Frame(subframe)
            btn_frame.pack(pady=2)

            start_btn = tk.Button(btn_frame, text="Start", command=lambda o=orientation: self.start(o))
            start_btn.grid(row=0, column=0, padx=2)

            stop_btn = tk.Button(btn_frame, text="Stop", command=lambda o=orientation: self.stop(o))
            stop_btn.grid(row=0, column=1, padx=2)

            replay_btn = tk.Button(btn_frame, text="Replay", command=lambda o=orientation: self.replay(o))
            replay_btn.grid(row=0, column=2, padx=2)

            self.figures[orientation] = fig
            self.canvases[orientation] = canvas
            self.axes[orientation] = ax
            self.animating[orientation] = False

        self.update_views()

        # Next/Prev subject keys
        self.master.bind("n", self.next_subject)
        self.master.bind("p", self.prev_subject)

    def go_to_subject(self):
        """Jump to subject based on entered subject number."""
        target = self.entry.get().strip()
        if not target:
            return

        # Find the index of the file matching this subject number
        for i, filepath in enumerate(self.file_list):
            subj = os.path.basename(filepath).split("_")[0]
            if subj == target:
                self.index = i
                self.load_subject(filepath)
                self.update_views()
                return

        # If no match found, update label
        self.label.config(text=f"Subject {target} not found")

    def load_subject(self, filepath):
        img = nib.load(filepath)
        self.data = img.get_fdata()
        self.subject_number = os.path.basename(filepath).split("_")[0]

        self.slice_indices = {
            'sagittal': 0,
            'coronal': 0,
            'axial': 0
        }

    def update_views(self):
        for orientation in ['sagittal', 'coronal', 'axial']:
            ax = self.axes[orientation]
            ax.clear()

            if orientation == 'sagittal':
                img_slice = self.data[self.slice_indices['sagittal'], :, :]
            elif orientation == 'coronal':
                img_slice = self.data[:, self.slice_indices['coronal'], :]
            else:  # axial
                img_slice = self.data[:, :, self.slice_indices['axial']]

            ax.imshow(np.rot90(img_slice), cmap="gray")
            ax.set_title(f"{orientation.capitalize()} (slice {self.slice_indices[orientation]})")
            ax.axis("off")

            self.canvases[orientation].draw()

        self.label.config(text=f"Subject: {self.subject_number}")

    def animate_slice(self, orientation):
        if not self.animating[orientation]:
            return

        axis = {'sagittal':0,'coronal':1,'axial':2}[orientation]
        max_index = self.data.shape[axis] - 2

        self.slice_indices[orientation] += 1
        if self.slice_indices[orientation] > max_index:
            self.animating[orientation] = False  # stop at end
            return

        self.update_views()
        self.master.after(self.speed, lambda: self.animate_slice(orientation))  # 100 ms per slice

    def start(self, orientation):
        if not self.animating[orientation]:
            self.animating[orientation] = True
            self.animate_slice(orientation)

    def stop(self, orientation):
        self.animating[orientation] = False

    def replay(self, orientation):
        self.slice_indices[orientation] = 0
        self.animating[orientation] = True
        self.animate_slice(orientation)

    def next_subject(self, event=None):
        if self.index < len(self.file_list) - 1:
            self.index += 1
            self.load_subject(self.file_list[self.index])
            self.update_views()

    def prev_subject(self, event=None):
        if self.index > 0:
            self.index -= 1
            self.load_subject(self.file_list[self.index])
            self.update_views()


if __name__ == "__main__":
    path = "/path/to/files/"
    files = sorted(glob(os.path.join(path, "*_3T_T1w_brain_overlay.nii.gz")))
    speed = 5 # change this for speed

    root = tk.Tk()
    root.geometry("1200x600")
    viewer = NiftiViewer(root, files, speed)
    root.mainloop()

