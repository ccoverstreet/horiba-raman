from horiba_raman_ccoverstreet import mapping
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

if __name__ == "__main__":
    #extra_spectra_to_files("Gd2O3_AlN_map_data.txt")

    x, y, intensity = mapping.parse_image("Gd2O3_AlN_map.txt")
    shift, pos, counts = mapping.parse_data_txt("Gd2O3_AlN_map_data.txt")


    maxes = []
    for i, c in enumerate(counts):
        m = mapping.extract_max_from_range(shift, c, 300, 400)
        print(i, pos[i], m)
        maxes.append(m)

    maxes = np.array(maxes)
    max_map = np.reshape(maxes, (6, 12))
    print(max_map)


    img = Image.open("Gd2O3_AlN_map.bmp")
    #plt.imshow(np.flip(intensity), extent=(x[0], x[-1], y[-1], y[0]))
    dx = np.abs(pos[0][0] - pos[1][0])
    dy = np.abs(pos[0][1] - pos[13][1])
    print(pos[0], pos[13])

    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.title(r"Overlay of Gd$_2$O$_3$ Raman peak", fontsize=16)
    plt.imshow(img, extent=(x[0], x[-1], y[-1], y[0]))
    plt.imshow(max_map, extent=(pos[0][0]-dx/2, pos[-1][0] + dx/2, pos[-1][1] + dy/2, pos[0][1] - dy/2), alpha=0.4, interpolation="bilinear")
    plt.annotate("AlN", (-280, 0), fontsize=16, ha="center")
    plt.annotate(r"Gd$_2$O$_3$", (295, 0), fontsize=16, ha="center")
    plt.xlim(x[0], x[-1])
    plt.ylim(y[-1], y[0])
    plt.xlabel(r"X [$\mu$m]", fontsize=16)
    plt.ylabel(r"Y [$\mu$m]", fontsize=16)

    plt.subplot(122)
    plt.imshow(img, extent=(x[0], x[-1], y[-1], y[0]))
    plt.imshow(intensity, extent=(x[0], x[-1], y[-1], y[0]))
    #plt.imshow(max_map, extent=(pos[0][0]-dx/2, pos[-1][0] + dx/2, pos[-1][1] + dy/2, pos[0][1] - dy/2), alpha=0.4, interpolation="bilinear")
    plt.xlim(x[0], x[-1])
    plt.ylim(y[-1], y[0])

    plt.xlabel(r"X [$\mu$m]", fontsize=16)
    plt.ylabel(r"Y [$\mu$m]", fontsize=16)

    plt.tight_layout()

    plt.savefig("Raman_mapping_postprocessing_demo.png")
    plt.show()

