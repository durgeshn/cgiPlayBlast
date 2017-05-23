import tempfile
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

reload(ImageDraw)


class Slate:
    def __init__(self, slate=True, band_size=20, font="arial", font_size=10, spacing=0,
                 logo_file=r'D:\temp\slate\logo.jpg'):
        """
        This Class is responsible for adding the slate to an image.
        With the data passed.
        With or without the slate bar.
        :param slate: for the slate bar. 
        :type slate: bool
        :param band_size: size for the slate bar 
        :type band_size: int
        :param font: font name
        :type font: str
        :param font_size: font size 
        :type font_size: int
        :param spacing: space between the 2 lines.
        :type spacing: int
        :param logo_file: logo if any provided.
        :type logo_file: str
        """
        self.temp_folder = tempfile.mkdtemp(prefix='cgiSlateMaker')
        self.comp_logo = logo_file
        self.font_size = font_size
        self.font = ImageFont.truetype(font, self.font_size)
        self.text_col = ''
        self.is_slate = slate
        self.band_size = band_size
        self.spacing = spacing

    @staticmethod
    def get_img(ima_path):
        """
        make the Image object for the given image.
        :param ima_path: file path for the image
        :type ima_path: file path
        :return: Image object
        :rtype: Image object
        """
        return Image.open(ima_path)

    def validate_images(self):
        pass

    @staticmethod
    def process_slate_data(**kwargs):
        """
        process the data as per the dict.
        :param kwargs: dict. for the slate data
        :type kwargs: dict
        :return: dict for slate
        :rtype: dict
        """
        slate_info = dict()
        for key, val in kwargs.iteritems():
            slate_info[key] = val
        return slate_info

    @staticmethod
    def validate_slate_data(dict_data):
        """
        this looks the data dict for the logo\Frame and checks if any other data is crashing 
        with them in the next line. 
        :param dict_data: slate data dict
        :type dict_data: dict
        :return: True or False
        :rtype: bool
        """
        for key, val in dict_data.iteritems():
            if val == 'logo' or val.startswith('Frame :'):
                if key in ['1', '2', '3', '7', '8', '9']:
                    if not a['%d' % (int(key) + 3)] == '':
                        return False
                if key in ['4', '5', '6', '10', '11', '12']:
                    if not a['%d' % (int(key) - 3)] == '':
                        return False
        return True

    def stripe_image(self, in_img):
        """
        weather to add strip to image or not.
        :param in_img: image file object
        :type in_img: Image object
        :return: image file object
        :rtype: Image object
        """
        in_img_size = in_img.size
        if self.is_slate:
            size_x = in_img_size[0]
            size_y = in_img_size[1] + (2 * self.band_size)
            band_img = Image.new('RGB', (size_x, size_y), (0, 0, 0))
            band_img.paste(in_img, (0, self.band_size))
            return band_img
        else:
            pass
        return in_img

    @property
    def get_logo(self):
        """
        This takes care of the logo part. Re-sizes the logo according to the slate bar.
        :return: logo img object
        :rtype: Imag object
        """
        logo = Image.open(self.comp_logo)
        # logo_w = logo.size[0]
        logo_h = logo.size[1]
        size = logo.size
        if self.band_size < logo_h:
            h_percent = (self.band_size / float(logo.size[1]))
            w_size = int((float(logo.size[0]) * float(h_percent)))
            size = (w_size, self.band_size)
        logo = logo.resize(size, Image.ANTIALIAS)
        return logo

    @staticmethod
    def save_image(in_img, out_file):
        """
        Save the Image object to the given location.
        :param in_img: in image object
        :type in_img: Image object
        :param out_file: path for the out file
        :type out_file: filePath
        :return: path for the out file
        :rtype: filePath
        """
        in_img.save(out_file, 'jpeg')
        return out_file

    def process_text(self, in_img, data_passed):
        """
        This is where the processing of the images happens.
        :param in_img: in image object
        :type in_img: Image object
        :param data_passed: slate data dict
        :type data_passed: dict
        :return: processed image object
        :rtype: Image object
        """
        draw = ImageDraw.Draw(in_img)
        length_part = in_img.size[0] / 3
        # space = self.font_size + self.spacing
        quad1 = (self.spacing, self.spacing)
        quad2 = (length_part + self.spacing, self.spacing)
        quad3 = ((length_part * 2) + self.spacing, self.spacing)

        quad4 = (self.spacing, (self.spacing + self.font_size))
        quad5 = (length_part + self.spacing, (self.spacing + self.font_size))
        quad6 = ((length_part * 2) + self.spacing, (self.spacing + self.font_size))

        quad7 = (self.spacing, (in_img.size[1] - 2 * (self.spacing + self.font_size)))
        quad8 = (length_part + self.spacing, (in_img.size[1] - 2 * (self.spacing + self.font_size)))
        quad9 = (2 * length_part + self.spacing, (in_img.size[1] - 2 * (self.spacing + self.font_size)))

        quad10 = (self.spacing, (in_img.size[1] - (self.spacing + self.font_size)))
        quad11 = (length_part + self.spacing, (in_img.size[1] - (self.spacing + self.font_size)))
        quad12 = (2 * length_part + self.spacing, (in_img.size[1] - (self.spacing + self.font_size)))

        print quad1, quad2, quad3, quad4, quad5, quad6, quad7 ,quad8 ,quad9, quad10, quad11, quad12

        if not self.validate_slate_data(dict_data=data_passed):
            return False

        for each_key in data_passed:
            quad = 'quad%s' % each_key
            if data_passed[each_key] == 'logo':
                quad_pass = eval(quad)
                pos_y = quad_pass[0]
                pos_x = quad_pass[1]
                if each_key in ['1', '2', '3', '4', '5', '6']:
                    pos_y = 0
                if each_key in ['7', '8', '9', '10', '11', '12']:
                    pos_y = in_img[1] - self.get_logo.size[0]
                if each_key in ['1', '4', '7', '10']:
                    pos_x = 0
                if each_key in ['3', '6', '9', '12']:
                    pos_x = in_img.size[0] - self.get_logo.size[0]
                quad_pass = (pos_x, pos_y)
                in_img.paste(self.get_logo, quad_pass)
                continue
            if data_passed[each_key]:
                draw.text(eval(quad), data_passed[each_key], (255, 255, 255), font=self.font)
        return in_img

    def process_all_images(self):
        pass


if __name__ == '__main__':
    sl = Slate(slate=True)
    img = sl.get_img(r'D:\temp\IMGS\img.0001.jpg')
    ret = sl.stripe_image(img)
    a = {'1': 'User : Durgesh.n', '2': 'FileName : TESTINGSCENE.ma', '3': '',
         '4': 'Date : 12/12/2017', '5': 'FINAL MOV', '6': 'logo',
         '7': 'CameraName : CamXXX', '8': 'focalLength : 60', '9': '',
         '10': '', '11': '', '12': '',
         }
    data = sl.process_slate_data(**a)
    ret = sl.process_text(ret, data)
    if ret:
        ret.show()
