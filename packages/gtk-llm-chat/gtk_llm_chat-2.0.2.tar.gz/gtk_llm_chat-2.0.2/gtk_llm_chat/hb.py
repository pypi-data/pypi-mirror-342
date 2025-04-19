import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class HeaderBarWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="HeaderBar Demo")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        # Crear HeaderBar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Título principal"
        hb.props.subtitle = "Este es el subtítulo"
        hb.props.has_subtitle = True
        # Esto es necesario para que el espacio del subtítulo se reserve
        self.set_titlebar(hb)

        # Agregar contenido a la ventana
        self.add(Gtk.TextView())


if __name__ == "__main__":
    win = HeaderBarWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
