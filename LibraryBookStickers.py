from PIL import Image, ImageDraw, ImageFont


class Sticker:
    def __init__(self, position_in_page=(None, None), author=None, library_location=None, isFiction=False):
        self.position = position_in_page
        self.author = author
        self.location = library_location
        self.isFiction = isFiction


class StickerSheet:
    A4_dim = (2480, 3508)  # in pixels
    default_sticker_table_dim = (11, 3)  # table cells

    def __init__(self, page_dim=A4_dim, table_dim=default_sticker_table_dim, stickers=[]):
        self.page_dim = page_dim
        self.table_dim = table_dim
        self.stickers = stickers

        # create empty white greyscale sheet
        self.canvas = Image.new(mode='L', size=self.page_dim, color=255)

    def add_sticker(self):
        pass

    def remove_sticker(self):
        pass

    def show_current_stickers(self):
        pass

    def save_to_file(self, file_name='Math Library Book Stickers.png', file_format='PNG'):
        # assemble actual image
        # make a blank image for the text, initialized to transparent text color
        txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

        # get a font
        fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
        # get a drawing context
        d = ImageDraw.Draw(txt)

        # draw text, half opacity
        d.text((10, 10), "Hello", font=fnt, fill=(255, 255, 255, 128))
        # draw text, full opacity
        d.text((10, 60), "World", font=fnt, fill=(255, 255, 255, 255))

        out = Image.alpha_composite(base, txt)

        out.show()

        # save final result to a PNG image file
        self.canvas.save(file_name, file_format)


if __name__ == '__main__':
    sheet = StickerSheet()
