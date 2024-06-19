from image_taker import ImageTaker
from processing.recontructor import reconstruct


def main():

    algorithm = "gridrec"
    n_tomos = 200
    n_flats = 20
    n_darks = 20
    url = "http://192.168.0.107:8080/video"

    sample_name = "sample"

    image_taker = ImageTaker(n_tomos, n_flats, n_darks, url)
    image_taker.get_tomos()
    image_taker.get_flats()
    image_taker.get_darks()
    image_taker.save_images(sample_name)

    tomos_3d, flats_3d, darks_3d = image_taker.get_3d_arrays()
    reconstruct(tomos_3d, flats_3d, darks_3d, sample_name, algorithm)


if __name__ == '__main__':
    main()
