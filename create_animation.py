import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from osgeo import gdal

def read_geotiff(filename):
    ds = gdal.Open(filename)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    return arr, ds

def show_plot(arr, title=""):
    plt.imshow(arr)
    plt.title(title)
    plt.colorbar()
    plt.show()

def load_images_from_folder(folder):
    images = []
    file_list = sorted(os.listdir(folder))
    for filename in file_list:
        img_path = os.path.join(folder, filename)
        img, _ = read_geotiff(img_path)
        if img is not None:
            images.append(img)
    return images


def leading_zero(n):
    return f"0{n}" if n < 10 else f"{n}"


def get_month(st_y, st_m, frame):
    m = 12 if (st_m + frame) % 12 == 0 else (st_m + frame) % 12
    y = (st_y) + (st_m + frame - 1) // 12
    return f"{y}-{leading_zero(m)}"

def convert_img(image):
    image = (image*400) + 1600

def create_animation(images, interval=100):
    fig, ax = plt.subplots()
    img_display = ax.imshow(images[0], vmin=1600, vmax=2000)
    plt.title("CH4 mean concentration over Svalbard (2016-2025)")
    fig.colorbar(img_display)
    
    def update(frame):
        img_display.set_array(images[frame])
        ax.text(420, 25, get_month(2016, 1, frame), bbox=dict(facecolor="white"))
        #ax.text(420, 25, get_month(2022, 1, frame), bbox=dict(facecolor="white"))
        return img_display
    
    ani = animation.FuncAnimation(fig, update, frames=len(images), interval=interval, blit=False)
    #plt.show()
    ani.save("./data/export/2016_2025_Svalbard_mean.gif")
    #ani.save("./data/export/2022_2025_Svalbard_mean.gif")
    return ani

if __name__ == "__main__":
    #folder_path = "./data/output_copernicus_mean/Svalbard_selected"
    folder_path = "./data/output_copernicus_mean/Svalbard"
    images = load_images_from_folder(folder_path)
    if images:
        create_animation(images, interval=100)
