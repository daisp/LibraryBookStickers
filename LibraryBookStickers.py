from PIL import Image, ImageDraw, ImageFont


class Sticker:
    def __init__(self, position_in_page: tuple = (None, None), author: str = None, library_location: int = None,
                 is_fiction: bool = False):
        self.position = position_in_page
        self.author = author
        self.location = library_location
        self.is_fiction = is_fiction


class StickerSheet:
    A4_dim = (2480, 3508)  # in pixels
    default_sticker_table_dim = (11, 3)  # table cells

    def __init__(self, page_dim: tuple = A4_dim, table_dim: tuple = default_sticker_table_dim, stickers: dict = {},
                 background_color: int = 255,
                 foreground_color: int = 0):
        self.page_dim = page_dim
        self.table_dim = table_dim
        self.stickers = stickers
        self.single_sticker_dim = self.__calculate_single_sticker_dim()
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)

        # create empty white greyscale sheet
        self.canvas = Image.new(mode='L', size=self.page_dim, color=self.background_color)

    def __calculate_single_sticker_dim(self):
        return int(self.page_dim[0] / self.table_dim[0]), int(self.page_dim[1] / self.table_dim[1])

    def add_sticker(self, sticker: Sticker):
        self.stickers[sticker.position] = sticker

    def remove_sticker(self, sticker: Sticker):
        self.stickers.pop(sticker.position)

    def show_current_stickers(self):
        print(self.stickers)

    def save_to_file(self, file_name='Math Library Book Stickers.png', file_format='PNG'):
        # assemble actual image

        for sticker in self.stickers:
            # make a blank image for the text
            sticker_img = Image.new('L', self.single_sticker_dim, color=self.background_color)

            # get a drawing context
            draw = ImageDraw.Draw(sticker_img)

            # draw text, half opacity
            draw.text((0, 0), self.stickers[sticker].author, font=self.font, fill=self.foreground_color)
            self.canvas.paste(sticker_img)

        # save final result to a PNG image file
        self.canvas.save(file_name, file_format)


if __name__ == '__main__':
    sheet = StickerSheet()
    my_sticker = Sticker((0, 0), 'ABC', 0, is_fiction=False)
    sheet.add_sticker(my_sticker)
    sheet.save_to_file()
