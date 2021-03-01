__docformat__ = "restructuredtext"
"""
The ui module contains the classes to easily build full screen user interface for your
games (or applications).

.. Important:: It works exclusively with the screen buffer system (place, delete,
   render, update, etc.).
   It doesn't work with Screen functions tagged "direct display" like display_at().

.. autosummary::
   :toctree: .

   UiConfig
   Dialog
   Box
   ProgressBar
   ProgressDialog
   VerticalProgressBar
   MessageDialog
"""
from pygamelib.assets import graphics
from pygamelib.gfx import core
from pygamelib import base, constants


class UiConfig(object):
    __instance = None

    def __init__(
        self,
        game=None,
        box_vertical_border=graphics.BoxDrawings.LIGHT_VERTICAL,
        box_horizontal_border=graphics.BoxDrawings.LIGHT_HORIZONTAL,
        box_top_left_corner=graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_RIGHT,
        box_top_right_corner=graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_LEFT,
        box_bottom_left_corner=graphics.BoxDrawings.LIGHT_ARC_UP_AND_RIGHT,
        box_bottom_right_corner=graphics.BoxDrawings.LIGHT_ARC_UP_AND_LEFT,
        fg_color=core.Color(255, 255, 255),
        bg_color=core.Color(0, 128, 128),
        border_fg_color=core.Color(255, 255, 255),
        border_bg_color=None,
        borderless_dialog=True,
    ):
        super().__init__()
        if game is None:
            raise base.PglInvalidTypeException(
                "UiConfig: the 'game' parameter cannot be None."
            )
        self.game = game
        self.box_vertical_border = box_vertical_border
        self.box_horizontal_border = box_horizontal_border
        self.box_top_left_corner = box_top_left_corner
        self.box_top_right_corner = box_top_right_corner
        self.box_bottom_left_corner = box_bottom_left_corner
        self.box_bottom_right_corner = box_bottom_right_corner
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.border_fg_color = border_fg_color
        self.border_bg_color = border_bg_color
        self.borderless_dialog = borderless_dialog

    @classmethod
    def instance(cls, *args, **kwargs):
        """Returns the instance of the UiConfig object

        Creates an UiConfig object on first call an then returns the same instance
        on further calls

        :return: Instance of Game object

        """
        if cls.__instance is None:
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance


class Dialog(object):
    def __init__(self, config=None) -> None:
        super().__init__()
        if config is None or not isinstance(config, UiConfig):
            raise base.PglInvalidTypeException(
                "The config parameter cannot be None and needs to be a UiConfig object."
            )
        setattr(self, "_config", config)
        setattr(self, "_user_input", "")

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        if isinstance(value, UiConfig):
            self._config = value
        else:
            raise base.PglInvalidTypeException(
                "Dialog.config = value: value needs to be an UiConfig object."
            )

    @property
    def user_input(self):
        return self._user_input

    @user_input.setter
    def user_input(self, value):
        if type(value) is str:
            self._user_input = value
        else:
            raise base.PglInvalidTypeException(
                "Dialog.user_input = value: value needs to be a str."
            )

    def show():
        raise NotImplementedError


class Box(object):
    def __init__(self, width, height, title="", config=None):
        super().__init__()
        self.__width = width
        self.__height = height
        self.__title = title
        self.__config = config
        self._cache = {}
        self._build_cache()

    def _build_cache(self):
        # Caching system to avoid tons of objects creations at rendering.
        self._cache["dialog_vertical_border"] = core.Sprixel(
            self.__config.box_vertical_border,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        self._cache["dialog_horizontal_border"] = core.Sprixel(
            self.__config.box_horizontal_border,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        self._cache["top_right_corner"] = core.Sprixel(
            self.__config.box_top_left_corner,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        self._cache["top_left_corner"] = core.Sprixel(
            self.__config.box_top_right_corner,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        self._cache["bottom_right_corner"] = core.Sprixel(
            self.__config.box_bottom_left_corner,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        self._cache["bottom_left_corner"] = core.Sprixel(
            self.__config.box_bottom_right_corner,
            self.__config.border_bg_color,
            self.__config.border_fg_color,
        )
        if isinstance(self.__title, base.Text):
            self._cache["title"] = self.__title
        else:
            self._cache["title"] = base.Text(
                self.__title,
                self.__config.border_fg_color,
                self.__config.border_bg_color,
            )
        self._cache["title_sprite"] = core.Sprite.from_text(self._cache["title"])

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        if isinstance(value, UiConfig):
            self.__config = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.config = value: value needs to be an UiConfig object."
            )

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if isinstance(value, base.Text) or type(value) is str:
            self.__title = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.title = value: value needs to be a Text object or str."
            )

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        if type(value) is int:
            self.__width = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.width = value: value needs to be an int."
            )

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        if type(value) is int:
            self.__height = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.width = value: value needs to be an int."
            )

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        vert_sprix = self._cache["dialog_vertical_border"]
        horiz_sprix = self._cache["dialog_horizontal_border"]
        buffer[row][column] = self._cache["top_right_corner"]
        if self._cache["title"] == "":
            for c in range(column + 1, column + self.__width - 1):
                buffer[row][c] = horiz_sprix
        else:
            for c in range(
                column + 1,
                column
                + 1
                + round(self.__width / 2 - len(self._cache["title"].text) / 2),
            ):
                buffer[row][c] = horiz_sprix
            self._cache["title_sprite"].render_to_buffer(
                buffer,
                row,
                column
                + 1
                + int(self.__width / 2 - 1 - len(self._cache["title"].text) / 2),
                buffer_height,
                buffer_width,
            )
            cs = (
                column
                + 1
                + int(self.__width / 2 - 1 - len(self._cache["title"].text) / 2)
                + len(self._cache["title"].text)
            )
            for c in range(
                cs, cs + int(self.__width / 2 - len(self._cache["title"].text) / 2)
            ):
                buffer[row][c] = horiz_sprix
        buffer[row][column + self.__width - 1] = self._cache["top_left_corner"]
        for r in range(1, self.__height - 1):
            buffer[row + r][column] = vert_sprix
            buffer[row + r][column + self.__width - 1] = vert_sprix
        buffer[row + self.__height - 1][column] = self._cache["bottom_right_corner"]
        for c in range(column + 1, column + self.__width - 1):
            buffer[row + self.__height - 1][c] = horiz_sprix
        buffer[row + self.__height - 1][column + self.__width - 1] = self._cache[
            "bottom_left_corner"
        ]


class ProgressBar(object):
    """
    A simple horizontal progress bar widget.

    :param value: The initial value parameter. It represents the progression.
    :type value: int
    :param maximum: The maximum value held by the progress bar. Any value over the
       maximum is ignored.
    :type maximum: int
    :param width: The width of the progress bar widget (in number of screen cells).
    :type width: int

    Example::

        # Create a default progress bar with the default configuration
        progress_bar = ProgressBar(config=UiConfig.instance())
        # Place the progress bar in the middle of the screen
        screen.place(
            progress_bar, screen.vcenter, screen.hcenter - int(progress_bar.width)
        )
        for progress in range(progress_bar.maximum + 1):
            # Do something useful
            progress_bar.value = progress
            screen.update()
    """

    def __init__(
        self,
        value=0,
        maximum=100,
        width=20,
        progress_marker=graphics.GeometricShapes.BLACK_RECTANGLE,
        empty_marker=" ",
        config=None,
    ):
        super().__init__()
        self.__value = value
        self.__maximum = maximum
        self.__width = width
        self.__progress_marker = progress_marker
        self.__empty_marker = empty_marker
        self.__config = config
        self._cache = {}
        self._build_cache()

    def _build_cache(self):
        if isinstance(self.__empty_marker, core.Sprixel):
            self._cache["pb_empty"] = self.__empty_marker
        else:
            self._cache["pb_empty"] = core.Sprixel(
                self.__empty_marker, self.__config.bg_color, self.__config.fg_color
            )
        if isinstance(self.__progress_marker, core.Sprixel):
            self._cache["pb_progress"] = self.__progress_marker
        else:
            self._cache["pb_progress"] = core.Sprixel(
                self.__progress_marker, self.__config.bg_color, self.__config.fg_color
            )

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        if isinstance(value, UiConfig):
            self.__config = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "Box.config(value): value needs to be an UiConfig object."
            )

    @property
    def progress_marker(self):
        return self.__progress_marker

    @progress_marker.setter
    def progress_marker(self, value):
        if isinstance(value, base.Text):
            self.__progress_marker = value.text
            self._cache["pb_progress"] = value
            self._build_cache()
        elif type(value) is str:
            self.__progress_marker = value
            self._cache["pb_progress"].text = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.progress_marker: value needs to be a str or "
                "pygamelib.base.Text."
            )
        self.__config.game.screen.trigger_rendering()

    @property
    def empty_marker(self):
        return self.__progress_marker

    @empty_marker.setter
    def empty_marker(self, value):
        if isinstance(value, base.Text):
            self.__empty_marker = value.text
            self._cache["pb_empty"] = value
            self._build_cache()
        elif type(value) is str:
            self.__empty_marker = value
            self._cache["pb_empty"].text = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.empty_marker: value needs to be a str or "
                "pygamelib.base.Text."
            )
        self.__config.game.screen.trigger_rendering()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if type(value) is int:
            self.__value = value
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.value: value needs to be an int."
            )
        self.__config.game.screen.trigger_rendering()

    @property
    def maximum(self):
        return self.__maximum

    @maximum.setter
    def maximum(self, value):
        if type(value) is int:
            self.__maximum = value
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.maximum: value needs to be an int."
            )
        self.__config.game.screen.trigger_rendering()

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        prog = min(int((self.__value * self.__width) / self.__maximum), self.__width)
        for c in range(0, prog):
            buffer[row][column + c] = self._cache["pb_progress"]
        for c in range(prog, self.__width):
            buffer[row][column + c] = self._cache["pb_empty"]


class ProgressDialog(Dialog):
    def __init__(
        self,
        label=base.Text("Progress dialog"),
        value=0,
        maximum=100,
        width=20,
        progress_marker=graphics.GeometricShapes.BLACK_RECTANGLE,
        empty_marker=" ",
        adaptive_width=True,
        destroy_on_complete=True,
        config=None,
    ):
        super().__init__(config=config)
        self.__label = label
        self.__value = value
        self.__maximum = maximum
        self.__width = width
        self.__progress_marker = progress_marker
        self.__empty_marker = empty_marker
        self.__adaptive_width = adaptive_width
        self.destroy_on_complete = destroy_on_complete
        self.__destroy = False
        # self.__config = config
        self._cache = {}
        self._build_cache()

    def _build_cache(self):
        if isinstance(self.__label, base.Text):
            self._cache["label"] = self.__label
        else:
            self._cache["label"] = base.Text(
                self.__label, self.config.fg_color, self.config.bg_color
            )
        # Adapt the width of the dialog based on the size of the text
        if self.__adaptive_width and self.__width != self._cache["label"].length:
            self.__width = len(self._cache["label"].text)
        self._cache["pb"] = ProgressBar(
            self.__value,
            self.__maximum,
            self.__width,
            self.__progress_marker,
            self.__empty_marker,
            config=self.config,
        )
        if not self.config.borderless_dialog:
            self._cache["borders"] = Box(
                self.__width, 2, self._cache["label"], config=self.config
            )

    # @property
    # def config(self):
    #     return self.__config

    # @config.setter
    # def config(self, value):
    #     if isinstance(value, UiConfig):
    #         self.__config = value
    #         self._build_cache()
    #     else:
    #         raise base.PglInvalidTypeException(
    #             "Box.config(value): value needs to be an UiConfig object."
    #         )

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        if isinstance(value, base.Text):
            self.__label = value.text
            self._cache["label"] = value
            self._build_cache()
        elif type(value) is str:
            self.__label = value
            self._cache["label"].text = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.label: value needs to be a str or pygamelib.base.Text."
            )
        self.config.game.screen.trigger_rendering()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if type(val) is int:
            self.__value = val
            self._cache["pb"].value = self.__value
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.value: value needs to be an int."
            )
        self.config.game.screen.trigger_rendering()

    @property
    def maximum(self):
        return self.__maximum

    @maximum.setter
    def maximum(self, value):
        if type(value) is int:
            self.__maximum = value
            self._build_cache()
        else:
            raise base.PglInvalidTypeException(
                "ProgressDialog.maximum: value needs to be an int."
            )
        self.config.game.screen.trigger_rendering()

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        if self.__destroy:
            self.config.game.screen.delete(row, column)
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            # We need to account for the borders in the box size
            box = Box(self.__width + 2, 4, config=self.config)
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        lbl = core.Sprite.from_text(self._cache["label"])

        lbl.render_to_buffer(
            buffer, row + offset, column + offset, buffer_height, buffer_width
        )
        self._cache["pb"].render_to_buffer(
            buffer, row + 1 + offset, column + offset, buffer_height, buffer_width
        )
        # prog = min(int((self.__value * self.__width) / self.__maximum), self.__width)
        # for c in range(0, prog):
        #     buffer[row + 1 + offset][column + c + offset] = self._cache["pb_progress"]
        # for c in range(prog, self.__width):
        #     buffer[row + 1 + offset][column + c + offset] = self._cache["pb_empty"]
        if self.destroy_on_complete and self.__value == self.__maximum:
            self.__destroy = True


class VerticalProgressBar(object):
    def __init__(
        self,
        value=0,
        maximum=100,
        height=10,
        progress_marker="#",
        empty_marker=" ",
        config=None,
    ):
        super().__init__()


class MessageDialog(Dialog):
    def __init__(self) -> None:
        super().__init__()


class LineInputDialog(Dialog):
    def __init__(
        self,
        label="Input a value:",
        default="",
        filter=constants.PRINTABLE_FILTER,
        config=None,
    ) -> None:
        super().__init__(config=config)
        self.__label = label
        self.__default = str(default)
        self.__filter = filter
        if self.__label is None or not (
            isinstance(self.__label, base.Text) or type(self.__label) is str
        ):
            raise base.PglInvalidTypeException(
                "LineInputDialog: label must be a str or pygamelib.base.Text."
            )
        if self.__default is None or not (
            isinstance(self.__default, base.Text) or type(self.__default) is str
        ):
            raise base.PglInvalidTypeException(
                "LineInputDialog: default must be a str."
            )
        if type(self.__label) is str:
            self.__label = base.Text(self.__label)
        self.user_input = self.__default

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        if isinstance(value, base.Text):
            self.__label = value.text
            self._cache["label"] = value
        elif type(value) is str:
            self.__label = value
            self._cache["label"].text = value
        else:
            raise base.PglInvalidTypeException(
                "LineInputDialog.label: value needs to be a str or pygamelib.base.Text."
            )
        self.config.game.screen.trigger_rendering()

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        offset = 0
        if not self.config.borderless_dialog:
            offset = 1
            # We need to account for the borders in the box size
            box = Box(self.__label.length + 2, 4, config=self.config)
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        lbl = core.Sprite.from_text(self.__label)
        lbl.render_to_buffer(
            buffer, row + offset, column + offset, buffer_height, buffer_width
        )
        inp = core.Sprite.from_text(base.Text(f"> {self.user_input}"))
        inp.render_to_buffer(
            buffer, row + 1 + offset, column + offset, buffer_height, buffer_width
        )

    def show(self):
        screen = self.config.game.screen
        game = self.config.game
        term = game.terminal
        inkey = ""
        screen.update()
        while 1:
            if inkey != "":
                if inkey.name == "KEY_ENTER":
                    break
                elif inkey.name == "KEY_ESCAPE":
                    self.user_input = ""
                    break
                elif inkey.name == "KEY_BACKSPACE" or inkey.name == "KEY_DELETE":
                    self.user_input = self.user_input[:-1]
                    screen.trigger_rendering()
                    screen.update()
                elif (
                    self.__filter == constants.PRINTABLE_FILTER and inkey.isprintable()
                ) or (self.__filter == constants.INTEGER_FILTER and inkey.isdigit()):
                    self.user_input += str(inkey)
                    screen.trigger_rendering()
                    screen.update()
            inkey = term.inkey(timeout=0.1)
        return self.user_input


class MultiLineInputDialog(Dialog):
    def __init__(
        self,
        fields=[
            {
                "label": "Input a value:",
                "default": "",
                "filter": constants.PRINTABLE_FILTER,
            }
        ],
        config=None,
    ) -> None:
        super().__init__(config=config)
        self.__fields = fields
        if self.__fields is None or not (type(self.__fields) is list):
            raise base.PglInvalidTypeException(
                "MultiInputDialog: fields must be a list of dictionaries."
            )
        self.user_input = ""
        self.__cache = list()
        self._build_cache()
        self.__current_field = 0

    def _build_cache(self):
        self.__cache = list()
        for field in self.__fields:
            if isinstance(field["label"], base.Text):
                self.__cache.append(field["label"])
            elif type(field["label"]) is str:
                self.__cache.append(base.Text(field["label"]))
            field["user_input"] = field["default"]

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, value):
        if type(value) is list:
            self.__fields = value
        else:
            raise base.PglInvalidTypeException(
                "MultiInputDialog.label: value needs to be a list of dictionaries."
            )
        self._build_cache()
        self.config.game.screen.trigger_rendering()

    def render_to_buffer(self, buffer, row, column, buffer_height, buffer_width):
        offset = 0
        max_text_width = 0
        if not self.config.borderless_dialog:
            # find the max width of the box
            for field in self.__fields:
                if (
                    isinstance(field["label"], base.Text)
                    and field["label"].length > max_text_width
                ):
                    max_text_width = field["label"].length
                elif (
                    type(field["label"]) is str and len(field["label"]) > max_text_width
                ):
                    max_text_width = len(field["label"])
            offset = 1
            # We need to account for the borders in the box size
            box = Box(
                max_text_width + 2, len(self.__fields) * 2 + 2, config=self.config
            )
            box.render_to_buffer(buffer, row, column, buffer_height, buffer_width)
        lc = 0
        fidx = 0
        for field in self.__fields:
            lbl = core.Sprite.from_text(self.__cache[fidx])
            lbl.render_to_buffer(
                buffer, row + offset + lc, column + offset, buffer_height, buffer_width
            )
            t = base.Text(f"> {field['user_input']}")
            if fidx == self.__current_field:
                t.fg_color = core.Color(0, 255, 0)
            inp = core.Sprite.from_text(t)
            inp.render_to_buffer(
                buffer,
                row + 1 + offset + lc,
                column + offset,
                buffer_height,
                buffer_width,
            )
            lc += 2
            fidx += 1

    def show(self):
        screen = self.config.game.screen
        game = self.config.game
        term = game.terminal
        inkey = ""
        screen.trigger_rendering()
        screen.update()
        self.__current_field = 0
        while 1:
            if inkey != "":
                if inkey.name == "KEY_ENTER":
                    break
                elif inkey.name == "KEY_TAB":
                    self.__current_field += 1
                    self.__current_field = self.__current_field % len(self.__fields)
                    screen.trigger_rendering()
                    screen.update()
                elif inkey.name == "KEY_ESCAPE":
                    for field in self.__fields:
                        field["user_input"] = ""
                    break
                elif inkey.name == "KEY_BACKSPACE" or inkey.name == "KEY_DELETE":
                    self.__fields[self.__current_field]["user_input"] = self.__fields[
                        self.__current_field
                    ]["user_input"][:-1]
                    screen.trigger_rendering()
                    screen.update()
                elif (
                    self.__fields[self.__current_field]["filter"]
                    == constants.PRINTABLE_FILTER
                    and inkey.isprintable()
                ) or (
                    self.__fields[self.__current_field]["filter"]
                    == constants.INTEGER_FILTER
                    and inkey.isdigit()
                ):
                    self.__fields[self.__current_field]["user_input"] += str(inkey)
                    screen.trigger_rendering()
                    screen.update()
            inkey = term.inkey(timeout=0.1)
        return self.__fields