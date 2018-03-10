import os
from PIL import Image

# By Cooper Nederhood (original)


def confirm_extension(state):
    '''
    Given a state, confirms that all training and testing 
    photos have extension .jpg and can be opened as an image

    Some image urls have a perfectly valid link but for some
    reason cannot be retrieved and were not filtered by other means.
    This required some handcleaning of the images data. This function does
    a first pass to assist in that handcleaning process by testing that the 
    image files are valid images files.
    '''

    open_file_errors = []
    jpg_ext_errors = []

    subfolder_names = ["Test", "Train"]

    for folder in subfolder_names:
        cur_path = state+"/"+folder
        lm_folders = os.listdir(cur_path)
        print("In {}:".format(cur_path))

        for lm in lm_folders:
            lm_path = cur_path+"/"+lm
            lm_pics = os.listdir(lm_path)
            print("*****In {}:".format(lm_path))

            for pic in lm_pics:
                print("***********pic={}".format(pic))

                f, e = os.path.splitext(pic)

                if e != ".jpg":
                    jpg_ext_errors.append(lm_path+"/"+pic)

                try:
                    img = Image.open(lm_path+"/"+pic)
                except:
                    open_file_errors.append(lm_path+"/"+pic)
                
    return open_file_errors, jpg_ext_errors   



rv = confirm_extension("Illinois_25per")

