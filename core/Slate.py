import tempfile
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
reload(ImageDraw)


class Slate:
    def __init__(self, slate=True, band_size=20, font="arial", font_size=10, spacing=0, logo_file=r'D:\temp\slate\logo.jpg'):
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
        return Image.open(ima_path)

    def validate_images(self):
        pass

    @staticmethod
    def process_slate_data(**kwargs):
        slate_info = dict()
        for key, val in kwargs.iteritems():
            slate_info[key] = val
        return slate_info

    @staticmethod
    def validate_slate_data(data):
        for key, val in data.iteritems():
            if val == 'logo' or val.startswith('Frame :'):
                if key in ['1', '2', '3', '7', '8', '9']:
                    if not a['%d' % (int(key) + 3)] == '':
                        return False
                if key in ['4', '5', '6', '10', '11', '12']:
                    if not a['%d' % (int(key) - 3)] == '':
                        return False
        return True

    def stripe_image(self, in_img):
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

    def add_logo(self, in_img, location=(0, 0)):
        logo = Image.open(self.comp_logo)
        logo_w = logo.size[0]
        logo_h = logo.size[1]
        size = logo.size
        if self.band_size < logo_h:
            h_percent = (self.band_size / float(logo.size[1]))
            w_size = int((float(logo.size[0]) * float(h_percent)))
            size = (w_size, self.band_size)
        logo = logo.resize(size, Image.ANTIALIAS)
        in_img.paste(logo, location)

    @staticmethod
    def save_image(in_img, out_file):
        in_img.save(out_file, 'jpeg')

    def process_text(self, in_img, data_passed):
        draw = ImageDraw.Draw(in_img)
        length_part = in_img.size[0] / 3
        space = self.font_size + self.spacing
        quad1 = (self.spacing, self.spacing)
        quad2 = (length_part + self.spacing, self.spacing)
        quad3 = ((length_part * 2) + self.spacing, self.spacing)

        quad4 = (self.spacing, (self.spacing+self.font_size))
        quad5 = (length_part + self.spacing, (self.spacing + self.font_size))
        quad6 = ((length_part * 2) + self.spacing, (self.spacing + self.font_size))

        quad7 = (self.spacing, (in_img.size[1] - 2*(self.spacing + self.font_size)))
        quad8 = (length_part + self.spacing, (in_img.size[1] - 2*(self.spacing + self.font_size)))
        quad9 = (2*length_part + self.spacing, (in_img.size[1] - 2*(self.spacing + self.font_size)))

        quad10 = (self.spacing, (in_img.size[1] - (self.spacing + self.font_size)))
        quad11 = (length_part + self.spacing, (in_img.size[1] - (self.spacing + self.font_size)))
        quad12 = (2*length_part + self.spacing, (in_img.size[1] - (self.spacing + self.font_size)))

        if not self.validate_slate_data(data=data_passed):
            return False

        for each_key in data_passed:
            quad = 'quad%s' % each_key
            if data_passed[each_key] == 'logo':
                quad = eval(quad)
                quad = (quad[0], quad[1]-self.spacing)

                self.add_logo(in_img=in_img, location=quad)
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
    a = {'1': 'User : Durgesh.n', '2': 'FileName : TESTINGSCENE.ma', '3': 'logo',
         '4': 'Date : 12/12/2017', '5': 'FINAL MOV', '6': '',
         '7': 'CameraName : CamXXX', '8': 'focalLength : 60', '9': 'Frame : 1',
         '10': '', '11': '', '12': '',
         }
    data = sl.process_slate_data(**a)
    ret = sl.process_text(ret, data)
    if ret:
        ret.show()
