import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

def parse_image(filename):
    """Parses the gray-scale image saved in .txt format as saved from the "Video" tab in LabSpec6

    Params: 
    - filename: path to txt file containing gray-scale image data and X/Y positions of pixels
    """

    with open(filename, encoding="latin-1") as f:
        x = None
        y = []
        vals = []
        for line in f:
            if line.startswith("#"):
                continue
            if line.startswith("\t"):
                x = [float(x) for x in line.split()]
            else:
                split = line.split()
                y.append(float(split[0]))
                vals.append([float(x) for x in split[1:]])
                

        print(len(x), len(vals[0]))
        print(y)

    return np.flip(np.array(x)), np.flip(np.array(y)), np.flip(np.array(vals))


def parse_data_txt(filename):
    """Parses the .txt version of the l6m file when saving in the browser tab or map tab with the spectral window highlighted

    Params: 
    - filename: path to txt file version of l6m file
    """
    with open(filename, encoding="latin-1") as f:
        shift = None
        pos = []
        counts = []
        for line in f:
            if line.startswith("#"): continue
            if line.startswith("\t"):
                shift = [float(x) for x in line.split()]
            else:
                split = line.split()
                pos.append((float(split[1]), float(split[0])))
                counts.append([float(x) for x in split[2:]])


    return np.array(shift), np.array(pos), np.array(counts)

def extra_spectra_to_files(filename, dirname="extracted-spectra"):
    """Extracts all raman spectra to a subdirectory from the .txt version of the l6m map file. The spatial position of spectra is included in extracted filename.

    Params:
    - filename: path to txt file version of l6m file"""
    os.makedirs(dirname, exist_ok=True)
    shift, pos, counts = parse_data_txt(filename)

    for i, p in enumerate(pos):
        stem = filename.replace(".txt", "")
        name = f"{stem}_{str(p[0]).replace(".", "p")}_{str(p[1]).replace(".", "p")}.dat"
        stack = np.vstack([shift, counts[i]]).T
        np.savetxt(f"{dirname}/{name}", stack)


def extract_max_from_range(x, y, x_min, x_max):
    start = np.argmax(x > x_min)
    end = np.argmax(x > x_max)

    return np.max(y[start:end])


