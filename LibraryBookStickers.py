from PIL import Image, ImageDraw, ImageFont


class Sticker:
    def __init__(self, position_in_page: tuple = (None, None), author: str = None, library_location: str = None,
                 is_fiction: bool = False, font_color: int = 0, background_color: int = 255, font_size: int = 50):
        self.position = position_in_page[::-1]
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
    default_sticker_grid_dim = (3, 11)  # grid cells

    def __init__(self, page_dim: tuple = A4_dim, grid_dim: tuple = default_sticker_grid_dim, stickers: dict = {},
                 background_color: int = 255):
        self.page_dim = page_dim
        self.grid_dim = grid_dim
        self.stickers = stickers
        self.single_sticker_dim = self.__calculate_single_sticker_dim()
        self.single_sticker_text_spawn_location = self.__calculate_single_sticker_text_spawn_location()
        self.background_color = background_color

        # create empty white greyscale sheet
        self.canvas = Image.new(mode='L', size=self.page_dim, color=self.background_color)

    def __calculate_single_sticker_dim(self) -> tuple:
        return int(self.page_dim[0] / self.grid_dim[0]), int(self.page_dim[1] / self.grid_dim[1])

    def __calculate_single_sticker_text_spawn_location(self) -> tuple:
        return int(self.single_sticker_dim[0] / 2), int(self.single_sticker_dim[1] / 2)

    def add_sticker(self, sticker: Sticker):
        self.stickers[sticker.position] = sticker

    def remove_sticker(self, sticker: Sticker):
        self.stickers.pop(sticker.position)

    def print_stickers_to_screen(self):
        print(self.stickers)

    def save_to_file(self, file_name='Math Library Book Stickers.png', file_format='PNG'):
        # assemble actual image from stickers
        for sticker_key in self.stickers:
            cur_sticker = self.stickers[sticker_key]
            # make a blank image for the text
            sticker_img = Image.new('L', self.single_sticker_dim, color=cur_sticker.background_color)

            # get a drawing context
            draw = ImageDraw.Draw(sticker_img)

            # draw text onto its frame
            draw.text(self.single_sticker_text_spawn_location, cur_sticker.get_sticker_text(), font=cur_sticker.font,
                      fill=cur_sticker.font_color)
            cur_sticker_2D_offset = (cur_sticker.position[0] * self.single_sticker_dim[0],
                                     cur_sticker.position[1] * self.single_sticker_dim[1])
            self.canvas.paste(sticker_img, box=cur_sticker_2D_offset)

        # save final result to a PNG image file
        self.canvas.save(file_name, file_format)


if __name__ == '__main__':
    sheet = StickerSheet()
    stickers = [Sticker((0, 0), 'ABC', '00', is_fiction=False),
                Sticker((0, 1), 'ABC', '01', is_fiction=False),
                Sticker((0, 2), 'ABC', '02', is_fiction=False),
                Sticker((1, 0), 'ABC', '03', is_fiction=False)]
    for sticker in stickers:
        sheet.add_sticker(sticker)
    sheet.save_to_file()
