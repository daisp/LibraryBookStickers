from PIL import Image, ImageDraw, ImageFont


class Sticker:
    def __init__(self, position_in_page: tuple = (None, None), author: str = None, library_location: str = None,
                 is_fiction: bool = False, font_color: int = 0, background_color: int = 255, font_size: int = 70):
        # reversing because pillow uses (column_number, row_number)
        self.position = position_in_page[::-1]
        self.position = (self.position[0] - 1,self.position[1] - 1)
        self.author = author
        self.location = library_location
        self.is_fiction = is_fiction
        self.font = ImageFont.truetype(
            'Pillow/Tests/fonts/FreeSans.ttf', font_size)
        # self.font = ImageFont.truetype('./times-new-roman.ttf', font_size)
        self.font_color = font_color
        self.background_color = background_color

    def get_sticker_text(self):
        return str(self.location) + '\n' + self.author


class StickerSheet:
    A4_dim = (2480, 3508)  # in pixels
    default_A4_horizontal_margins = 0  # in pixels
    # default_A4_vertical_margins = (12 / 297) * A4_dim[1]  # in pixels
    default_A4_vertical_margins = int((11 / 297) * A4_dim[1])  # in pixels
    default_sticker_grid_dim = (3, 11)  # grid cells: (columns_num, rows_num)
    default_fiction_icon_path = './fiction_icon.jpg'
    default_fiction_icon_resize_factor = 0.18
    default_empty_stickers_dict = {}

    def __init__(self, page_dim: tuple = A4_dim, grid_dim: tuple = default_sticker_grid_dim,
                 stickers: dict = default_empty_stickers_dict,
                 background_color: int = 255, horizontal_margins: int = default_A4_horizontal_margins,
                 vertical_margins: int = default_A4_vertical_margins,
                 fiction_icon_path=default_fiction_icon_path,
                 fiction_icon_resize_factor=default_fiction_icon_resize_factor):

        # preliminary setup
        self.stickers = stickers
        self.page_dim, self.horizontal_margins, self.vertical_margins = page_dim, horizontal_margins, vertical_margins
        self.grid_dim, self.background_color = grid_dim, background_color

        self.__calculate_single_sticker_dim()
        self.__initialize_fiction_icon(
            fiction_icon_path, fiction_icon_resize_factor)
        self.__initialize_sheet_canvas()

    def __initialize_fiction_icon(self, fiction_icon_path: str, fiction_icon_resize_factor: float):
        self.fiction_icon = Image.open(fiction_icon_path)
        self.fiction_icon = self.fiction_icon.resize((int(self.fiction_icon.size[0] * fiction_icon_resize_factor),
                                                      int(self.fiction_icon.size[1] * fiction_icon_resize_factor)))
        self.fiction_icon_dim = self.fiction_icon.size

    def __initialize_sheet_canvas(self):
        self.canvas = Image.new(
            mode='L', size=self.page_dim, color=self.background_color)

    def __calculate_single_sticker_dim(self):
        self.single_sticker_dim = int((self.page_dim[0] - 2 * self.horizontal_margins) / self.grid_dim[0]), \
            int((self.page_dim[1] - 2 *
                 self.vertical_margins) / self.grid_dim[1])

    def __calculate_single_sticker_location_text_offset(self, text: str, draw_context: ImageDraw.Draw,
                                                        font=None) -> tuple:
        text_size = draw_context.textsize(text, font=font)
        return int((self.single_sticker_dim[0] - text_size[0]) / 2), int(self.single_sticker_dim[1] * 0.29)

    def __calculate_single_sticker_author_text_offset(self, text: str, draw_context: ImageDraw.Draw,
                                                      font=None) -> tuple:
        text_size = draw_context.textsize(text, font=font)
        return int((self.single_sticker_dim[0] - text_size[0]) / 2), int(self.single_sticker_dim[1] * 0.58)

    def add_sticker(self, new_sticker: Sticker):
        self.stickers[new_sticker.position] = new_sticker

    def remove_sticker(self, sticker_to_remove: Sticker):
        self.stickers.pop(sticker_to_remove.position)

    def print_stickers_to_screen(self):
        print(self.stickers)

    def save_to_file(self, file_name: str = 'Math Library Book Stickers.png', file_format: str = 'PNG'):
        # assemble actual image from stickers
        for sticker_key in self.stickers:
            cur_sticker = self.__get_current_sticker(sticker_key)
            draw, sticker_img = self.__initialize_blank_sticker(sticker_dim=self.single_sticker_dim,
                                                                background_color=cur_sticker.background_color)

            # calculate text offsets for the current sticker
            location_text_offset, author_text_offset = self.__calculate_sticker_text_offsets(cur_sticker=cur_sticker,
                                                                                             draw_context=draw)

            # draw text onto the sticker according to the offset we just calculated
            self.__draw_sticker_text(cur_sticker=cur_sticker, location_text_offset=location_text_offset,
                                     author_text_offset=author_text_offset, draw_context=draw)

            # add fiction icon if necessary
            if cur_sticker.is_fiction:
                self.__paste_fiction_icon_onto_sticker(sticker_img=sticker_img)

            # adding the currently built sticker to the final sheet at its desired position in the grid
            self.__paste_sticker_to_grid(
                cur_sticker=cur_sticker, sticker_img=sticker_img)

        # after pasting all necessary stickers onto sheet, save the final result to a PNG image file
        self.__save_sheet_to_file(file_name, file_format)

    def __calculate_sticker_text_offsets(self, cur_sticker: Sticker, draw_context: ImageDraw.Draw):
        location_offset = self.__calculate_single_sticker_location_text_offset(text=cur_sticker.location,
                                                                               draw_context=draw_context,
                                                                               font=cur_sticker.font)
        author_offset = self.__calculate_single_sticker_author_text_offset(text=cur_sticker.author,
                                                                           draw_context=draw_context,
                                                                           font=cur_sticker.font)

        return location_offset, author_offset

    def __get_current_sticker(self, sticker_key):
        return self.stickers[sticker_key]

    @staticmethod
    def __initialize_blank_sticker(sticker_dim, background_color):
        # create a blank image for the text
        sticker_img = Image.new('L', size=sticker_dim, color=background_color)

        # create a drawing context
        draw = ImageDraw.Draw(sticker_img)

        return draw, sticker_img

    @staticmethod
    def __draw_sticker_text(cur_sticker: Sticker, location_text_offset, author_text_offset,
                            draw_context: ImageDraw.Draw):
        draw_context.text(location_text_offset, cur_sticker.location, font=cur_sticker.font,
                          fill=cur_sticker.font_color, draw_context=draw_context)
        draw_context.text(author_text_offset, cur_sticker.author, font=cur_sticker.font,
                          fill=cur_sticker.font_color, draw_context=draw_context)

    def __paste_fiction_icon_onto_sticker(self, sticker_img: Image):
        sticker_img.paste(self.fiction_icon,
                          (int(self.single_sticker_dim[0] / 2 - self.fiction_icon_dim[0] / 2),
                           int(0.05 * self.single_sticker_dim[1])))

    def __paste_sticker_to_grid(self, cur_sticker: Sticker, sticker_img: Image):
        cur_sticker_2D_pixel_offset_in_sheet = (
            self.horizontal_margins +
            cur_sticker.position[0] * self.single_sticker_dim[0],
            self.vertical_margins + cur_sticker.position[1] * self.single_sticker_dim[1])

        self.canvas.paste(
            sticker_img, box=cur_sticker_2D_pixel_offset_in_sheet)

    def __save_sheet_to_file(self, file_name, file_format):
        self.canvas.save(file_name, file_format)


if __name__ == '__main__':
    sheet = StickerSheet()
    stickers = [Sticker((5, 2), 'PIN', '35')

                ]
    for sticker in stickers:
        sheet.add_sticker(sticker)
    sheet.save_to_file()
