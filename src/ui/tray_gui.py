from pystray import Icon, Menu, MenuItem

from PIL import Image, ImageDraw


class TrayGui:
    def __create_image(self, width, height, fgcolor, fg2color, bgcolor):
        image = Image.new("RGB", (width, height), bgcolor)
        dc = ImageDraw.Draw(image)

        dc.ellipse(xy=(0, 0, width, height), width=6, outline=fgcolor)
        dc.line(xy=(15, 10, width / 2, height / 2), fill=fgcolor, width=8)
        dc.line(xy=(width / 2, height / 2, 58, height / 2), fill=fg2color, width=8)

        return image

    def __create_menu(self) -> Menu:
        menu_items = [
            MenuItem("Start/Stop Work", action=self.__on_startstop_work_clicked),
        ]
        menu = Menu(*menu_items)

        return menu

    def __on_startstop_work_clicked(self, icon: Icon, item: str):
        print(f"{item} clicked")

    def start(self):
        icon = Icon(
            "PyTimeTrack",
            icon=self.__create_image(64, 64, "#C8E6C9", "#81C784", "#455A64"),
            menu=self.__create_menu(),
        )

        icon.run()
