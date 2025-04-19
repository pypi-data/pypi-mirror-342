import argparse
import re
import subprocess
import sys
import time

from Xlib import X, display, xobject

PARSER = argparse.ArgumentParser(description='Opens and x11 application at a particular point')
PARSER.add_argument("geometry", help="Where are how big the window should be. Of the form (widthxheight)?[+-]x[+-y]. See README (--open-readme) for details")
PARSER.add_argument("--open-readme", action='store_true', help="Open the README file")
PARSER.add_argument("command", nargs='*', help="Command to run. Use -- before options with -")


def main():

    geometry = sys.argv[1] # work around to allow geometry to start with -
    args = PARSER.parse_args(["placeholder"] + sys.argv[2:])
    args.geometry = geometry

    p = subprocess.Popen(args.command)

    d = display.Display()
    root = d.screen().root

    if args.open_readme:
        subprocess.check_call(["open",  "http://github.com/talwrii/x-open-point"])

    start = time.time()
    while True:
        windows = root.get_full_property(
            d.intern_atom('_NET_CLIENT_LIST', True), X.AnyPropertyType).value

        found_window = None
        for window_id in windows:
            window = d.create_resource_object('window', window_id)

            window_pid = window.get_full_property(
                d.intern_atom("_NET_WM_PID", True), X.AnyPropertyType).value[0]

            if window_pid == p.pid:
                found_window = window_id
                break

        if found_window:
            break

        time.sleep(0.2)

        if time.time() - start > 3:
            raise Exception('Timed out waiting for window with pid')

    win = xobject.drawable.Window(d.display, found_window)

    geom = win.get_geometry()
    width = geom._data["width"] #pylint: disable=protected-access
    height = geom._data["height"] #pylint: disable=protected-access

    x, y, width, height = parse_geometry(d.screen(), args.geometry, width, height)

    if x is not None:
        win.configure(x=x)
    if y is not None:
        win.configure(y=y)
    if width:
        win.configure(width=width)
    if height:
        win.configure(height=height)

    d.sync()


def parse_value(v, maximum):
    if v[-1] == "%":
        return int(float(v[:-1]) / 100 * maximum)
    else:
        return int(v)


def parse_geometry(screen, x, width, height):
    screen_width = screen.width_in_pixels
    screen_height = screen.height_in_pixels


    parts = re.split("([+-])", x)

    if len(parts) >= 2:
        size, split, *rest = parts
    else:
        size = parts[0]
        split = None
        rest = None

    if size != "":
        width_str, height_str = size.split("x")
        width = parse_value(width_str, screen_width)
        height = parse_value(height_str, screen_height)

    if rest == None:
        x = y = None
    else:
        position = split + "".join(rest)
        _, x_sign, x_str, y_sign, y_str = re.split("([+-])", position)

        x = parse_value(x_str, screen_width)
        y = parse_value(y_str, screen_height)

        if x_sign == "-":
            x = screen_width - width - x

        if y_sign == "-":
            y = screen_height - height - y

    return x, y, width, height
