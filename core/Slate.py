import tempfile
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Slate:
    def __init__(self, new=True, start_frame=0, font="Arial.ttf", font_size=20):
        self.temp_folder = tempfile.mkdtemp(prefix='cgiSlateMaker')
        self.comp_logo = ''
        self.font = ImageFont.truetype("Arial.ttf", 20)
        self.font_size = font_size
        self.text_col = ''
        self.is_new = new
        self.start_frame = start_frame

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

    def stripe_image(self, in_img):
        # in_img = Image.open(in_image)
        in_img_size = in_img.size
        if not self.is_new:
            band_size = (in_img_size[0], 70)
            band_img = Image.new("RGB", band_size)
            # slap the bands on top and bottom
            in_img.paste(band_img, (0, 0))
            in_img.paste(band_img, (0, in_img_size[1] - 70))
        else:
            pass
        return in_img

    def add_logo(self, in_img):
        logo = Image.open(self.comp_logo)
        base_h = 70
        percentage_change = base_h / float(logo.size[1])
        horizontal_size = int((float(logo.size[0]) * float(percentage_change)))
        logo = logo.resize((horizontal_size, base_h), Image.ANTIALIAS)
        in_img.paste(logo, (in_img.size[0] - (horizontal_size + 200), in_img.size[1] - 70))

    @staticmethod
    def save_image(in_img, out_file):
        in_img.save(out_file, 'jpeg')

    def process_text(self, in_img, data_passed):
        draw = ImageDraw.Draw(in_img)
        length_part = in_img.size[0] / 3
        quad1 = (10, 10)
        quad2 = (length_part + 170, 10)
        quad3 = ((length_part * 2) + 200, 10)

        quad4 = (10, 45)
        quad5 = (length_part + 170, 45)
        quad6 = ((length_part * 2) + 200, 45)

        quad7 = (10, (in_img.size[1] - 70))
        quad8 = (length_part + 170, (in_img.size[1] - 70))
        quad9 = (length_part + 170, (in_img.size[1] - 70))

        quad10 = (10, (in_img.size[1] - 35))
        quad11 = (length_part + 170, (in_img.size[1] - 35))
        quad12 = (length_part + 170, (in_img.size[1] - 35))

        for each_key in data_passed:
            quad = 'quad%s' % each_key
            print quad
            draw.text(quad, data_passed[each_key], (255, 255, 255), font=self.font)

        # top1 Quad.
        # draw.text(quad1_1, "Sample Text", (255, 255, 255), font=self.font)
        # draw.text(quad1_2, "Sample Text", (255, 255, 255), font=self.font)
        # draw.text(quad1_3, "Sample Text", (255, 255, 255), font=self.font)
        #
        # # top2 Quad.
        # draw.text(quad2_1, "Sample Text", (255, 255, 255), font=self.font)
        # draw.text(quad2_2, "Sample Text", (255, 255, 255), font=self.font)
        # draw.text(quad2_3, "Sample Text", (255, 255, 255), font=self.font)
        #
        # # bottom1 Quad.
        # draw.text(quad3_1, "Sample Text", (255, 255, 255), font=self.font)
        # draw.text(quad3_2, "Sample Text", (255, 255, 255), font=self.font)
        # draw.text(quad3_3, "Sample Text", (255, 255, 255), font=self.font)
        #
        # # bottom1 Quad.
        # draw.text(quad4_1, "Sample Text", (255, 255, 255), font=self.font)
        # draw.text(quad4_2, "Sample Text", (255, 255, 255), font=self.font)
        # draw.text(quad4_3, "Sample Text", (255, 255, 255), font=self.font)

        return in_img

    def process_all_images(self):
        pass


if __name__ == '__main__':
    print 1
    sl = Slate(new=False)
    img = sl.get_img('C:/Users/durgesh.n/appdata/local/temp/cgiCompile_kqpv1m/out-001.jpg')
    ret = sl.stripe_image(img)
    a = {'1': 'a', '2': 'b', '3': 'c',
         '4': 'a', '5': 'b', '6': 'c'
         }
    data = sl.process_slate_data(**a)
    ret = sl.process_text(img, data)
    ret.show()
