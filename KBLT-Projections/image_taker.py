import numpy as np

from logger import LOGGER
from components.camera import Camera
from components.microphone import Microphone
from components.image import Image
import cv2 as cv
import os
import time
from skimage import color


class ImageTaker:
    def __init__(self, n_tomos, n_flats, n_darks, url):

        self.n_tomos, self.tomos = n_tomos, []
        self.n_flats, self.flats = n_flats, []
        self.n_darks, self.darks = n_darks, []

        self.camera = Camera(url)
        self.microphone = Microphone()

    def get_tomos(self):

        try:
            while len(self.tomos) < self.n_tomos:

                ret, frame = self.camera.get_ret_frame()
                cv.imshow("Tomograms", frame)
                #cv.waitKey(1)
                if self.microphone.is_vibrating():
                    image = Image(frame, 'tomo', '.tiff', color_model="RGB")
                    self.tomos.append(image)
                    LOGGER.info(f"Tomo nr {len(self.tomos)} taken")
                    time.sleep(0.9)


        except KeyboardInterrupt:
            LOGGER.info("Keyboard interrupt received. Cleaning...")
            self.microphone.clean()
            LOGGER.info("Exiting...")

        # Release the window
        cv.destroyAllWindows()


    def get_flats(self):
        LOGGER.info("Start tanking Flats")
        self._capture("flat", ".tiff", self.flats, self.n_flats)

    def get_darks(self):
        LOGGER.info("Start tanking Darks")
        self._capture("dark", ".tiff", self.darks, self.n_darks)
        self.camera.clean()



    def save_images(self, sample_name):
        tomos_path, flats_path, darks_path = self._create_folders(sample_name)

        save_images_type = [('tomo', self.tomos, tomos_path), ('flat', self.flats, flats_path),
                            ('dark', self.darks, darks_path)]

        for image_type, images, path in save_images_type:
            for i, image in enumerate(images):
                image_path = os.path.join(path, f"{image_type}_{'%04d' % (i + 1)}{image.get_extension()}")
                image = convert_to_grayscale(image)
                cv.imwrite(image_path, image.get_array())
            LOGGER.info(f"16-bit grayscale {image_type.upper()}S saved successfully in '{path}'")

    def _capture(self, mode, extension, images_list, n_photos):
        photo_taken = 0
        while len(images_list) < n_photos:
            ret, frame = self.camera.get_ret_frame()
            cv.imshow("Press enter to take photo", frame)
            key = cv.waitKey(1)
            if key == 32:
                image = Image(frame, mode, extension, color_model="RGB")
                images_list.append(image)
                photo_taken += 1
                LOGGER.info(f"{mode} nr {len(images_list)} taken")














    def _create_folders(self, sample_name):
        base_path = "output"
        sample_path = os.path.join(base_path, sample_name)

        # Check if the sample folder already exists
        if os.path.exists(sample_path):
            # If it exists, find an available name
            i = 2
            while True:
                new_sample_name = f"{sample_name}_{i}"
                new_sample_path = os.path.join(base_path, new_sample_name)
                if not os.path.exists(new_sample_path):
                    sample_path = new_sample_path
                    break
                i += 1

        # Create the necessary folders
        projections_path = os.path.join(sample_path, "projections")
        tomos_path = os.path.join(projections_path, "tomos")
        flats_path = os.path.join(projections_path, "flats")
        darks_path = os.path.join(projections_path, "darks")

        os.makedirs(tomos_path, exist_ok=True)
        os.makedirs(flats_path, exist_ok=True)
        os.makedirs(darks_path, exist_ok=True)

        return tomos_path, flats_path, darks_path


    # TODO QUESTO MI SEMBRA INUTILE? BASTA CHE FAI WRAPPI N[P.ARRAY()
    def get_3d_arrays(self):
        # Get shape of a single image (resolution), it should be the same for tomos, flats and dark
        resolution = self.tomos[0].get_array().shape
        tomo_3d = np.empty((len(self.tomos), resolution[0], resolution[1]))
        flat_3d = np.empty((len(self.flats), resolution[0], resolution[1]))
        dark_3d = np.empty((len(self.darks), resolution[0], resolution[1]))
        for i, tomo in enumerate(self.tomos):
            tomo_3d[i, :, :] = tomo.get_array()
        for i, flat in enumerate(self.flats):
            flat_3d[i, :, :] = flat.get_array()
        for i, dark in enumerate(self.darks):
            dark_3d[i, :, :] = dark.get_array()

        return tomo_3d, flat_3d, dark_3d



def convert_to_grayscale(image):
    conversion_factor = 32767
    image.set_color_model('grayscale')
    gray_array = color.rgb2gray(image.get_array()) * conversion_factor
    gray_array = gray_array.astype(np.int16)
    image.set_array(gray_array)
    return image
