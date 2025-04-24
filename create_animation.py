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
    file_list = sorted(os.listdir(folder))  # Sortowanie plików w folderze
    for filename in file_list:
        img_path = os.path.join(folder, filename)
        img, _ = read_geotiff(img_path)
        if img is not None:
            images.append(img)
    return images

def create_animation(images, interval=100):
    fig, ax = plt.subplots()
    img_display = ax.imshow(images[0])
    plt.title("CH4 concentration - Svalbard (2024)")
    
    def update(frame):
        img_display.set_array(images[frame])
        return img_display
    
    ani = animation.FuncAnimation(fig, update, frames=len(images), interval=interval, blit=False)
    #plt.show()
    ani.save("./output/2024_Svalbard_mean.gif")
    return ani

if __name__ == "__main__":
    folder_path = "./ch4_data/Svalbard_mean/"  # Zmień na właściwą ścieżkę
    images = load_images_from_folder(folder_path)
    if images:
        create_animation(images, interval=100)
