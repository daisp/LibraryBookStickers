from PIL import Image, ImageDraw, ImageFont


class Sticker:
    def __init__(self, position_in_page: tuple = (None, None), author: str = None, library_location: str = None,
                 is_fiction: bool = False, font_color: int = 0, background_color: int = 255, font_size: int = 90):
        self.position = position_in_page[::-1]  # reversing because pillow uses (column_number, row_number)
        self.author = author
        self.location = library_location
        self.is_fiction = is_fiction
        self.font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', font_size)
        self.font_color = font_color
        self.background_color = background_color

    def get_sticker_text(self):
        return str(self.location) + '\n' + self.author


class StickerSheet:
    A4_dim = (2480, 3508)  # in pixels
    default_A4_horizontal_margins = 0  # in pixels
    # default_A4_vertical_margins = (12 / 297) * A4_dim[1]  # in pixels
    default_A4_vertical_margins = int((12 / 297) * A4_dim[1])  # in pixels
    default_sticker_grid_dim = (3, 11)  # grid cells: (columns_num, rows_num)
    default_fiction_icon_path = './fiction_icon.jpg'
    default_fiction_icon_resize_factor = 0.18

    def __init__(self, page_dim: tuple = A4_dim, grid_dim: tuple = default_sticker_grid_dim, stickers: dict = {},
                 background_color: int = 255, horizontal_margins: int = default_A4_horizontal_margins,
                 vertical_margins: int = default_A4_vertical_margins,
                 fiction_icon_path=default_fiction_icon_path,
                 fiction_icon_resize_factor=default_fiction_icon_resize_factor):
        self.page_dim = page_dim
        self.horizontal_margins = horizontal_margins
        self.vertical_margins = vertical_margins
        self.grid_dim = grid_dim
        self.stickers = stickers
        self.single_sticker_dim = self.__calculate_single_sticker_dim()
        self.single_sticker_location_text_offset = None  # self.__calculate_single_sticker_location_text_offset()
        self.single_sticker_author_text_offset = None  # self.__calculate_single_sticker_author_text_offset()
        self.background_color = background_color
        self.fiction_icon = Image.open(fiction_icon_path)
        self.fiction_icon = self.fiction_icon.resize((int(self.fiction_icon.size[0] * fiction_icon_resize_factor),
                                                      int(self.fiction_icon.size[1] * fiction_icon_resize_factor)))
        self.fiction_icon_dim = self.fiction_icon.size

        # create empty white greyscale sheet
        self.canvas = Image.new(mode='L', size=self.page_dim, color=self.background_color)

    def __calculate_single_sticker_dim(self) -> tuple:
        return int((self.page_dim[0] - 2 * self.horizontal_margins) / self.grid_dim[0]), \
               int((self.page_dim[1] - 2 * self.vertical_margins) / self.grid_dim[1])

    def __calculate_single_sticker_location_text_offset(self, text: str, draw_context: ImageDraw.Draw,
                                                        font=None) -> tuple:
        text_size = draw_context.textsize(text, font=font)
        return int((self.single_sticker_dim[0] - text_size[0]) / 2), int(self.single_sticker_dim[1] * 0.3)

    def __calculate_single_sticker_author_text_offset(self, text: str, draw_context: ImageDraw.Draw,
                                                      font=None) -> tuple:
        text_size = draw_context.textsize(text, font=font)
        return int((self.single_sticker_dim[0] - text_size[0]) / 2), int(self.single_sticker_dim[1] * 0.6)

    def add_sticker(self, new_sticker: Sticker):
        self.stickers[new_sticker.position] = new_sticker

    def remove_sticker(self, sticker_to_remove: Sticker):
        self.stickers.pop(sticker_to_remove.position)

    def print_stickers_to_screen(self):
        print(self.stickers)

    def save_to_file(self, file_name: str = 'Math Library Book Stickers.png', file_format: str = 'PNG'):
        # assemble actual image from stickers
        for sticker_key in self.stickers:
            cur_sticker = self.stickers[sticker_key]
            # make a blank image for the text
            sticker_img = Image.new('L', self.single_sticker_dim, color=cur_sticker.background_color)

            # get a drawing context
            draw = ImageDraw.Draw(sticker_img)

            # calculate text offsets in the current sticker
            self.single_sticker_location_text_offset = self.__calculate_single_sticker_location_text_offset(
                text=cur_sticker.location, draw_context=draw, font=cur_sticker.font)
            self.single_sticker_author_text_offset = self.__calculate_single_sticker_author_text_offset(
                text=cur_sticker.author, draw_context=draw, font=cur_sticker.font)

            # draw text onto the sticker
            draw.text(self.single_sticker_location_text_offset, cur_sticker.location, font=cur_sticker.font,
                      fill=cur_sticker.font_color, draw_context=draw)
            draw.text(self.single_sticker_author_text_offset, cur_sticker.author, font=cur_sticker.font,
                      fill=cur_sticker.font_color, draw_context=draw)

            # add fiction icon if necessary
            if cur_sticker.is_fiction:
                sticker_img.paste(self.fiction_icon,
                                  (int(self.single_sticker_dim[0] / 2 - self.fiction_icon_dim[0] / 2),
                                   int(0.05 * self.single_sticker_dim[1])))

            cur_sticker_2D_pixel_offset_in_sheet = (
                self.horizontal_margins + cur_sticker.position[0] * self.single_sticker_dim[0],
                self.vertical_margins + cur_sticker.position[1] * self.single_sticker_dim[1])

            self.canvas.paste(sticker_img, box=cur_sticker_2D_pixel_offset_in_sheet)

        # save final result to a PNG image file
        self.canvas.save(file_name, file_format)


if __name__ == '__main__':
    sheet = StickerSheet()
    stickers = [Sticker((0, 0), 'ABC', '00', is_fiction=True),
                Sticker((0, 1), 'ABC', '01', is_fiction=False),
                Sticker((0, 2), 'ABC', '02', is_fiction=True),
                Sticker((1, 0), 'ABC', '02', is_fiction=True),
                Sticker((1, 1), 'ABC', '02', is_fiction=True),
                Sticker((1, 2), 'ABC', '02', is_fiction=True),
                Sticker((2, 0), 'ABC', '02', is_fiction=True),
                Sticker((2, 1), 'ABC', '02', is_fiction=True),
                Sticker((2, 2), 'ABC', '02', is_fiction=True),
                Sticker((3, 0), 'ABC', '02', is_fiction=True),
                Sticker((3, 1), 'ABC', '03', is_fiction=False)]
    for sticker in stickers:
        sheet.add_sticker(sticker)
    sheet.save_to_file()
