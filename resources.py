import os, pygame, sys, tempfile, json, atexit

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


APPICON = pygame.image.load(resource_path("data/Logo.png"))


checkSVGpath = resource_path("data/check.svg")
jsonTheme = {
  "defaults": {
    "colours": {
      "normal_bg": "#e08b81",
      "hovered_bg": "#fbda91",
      "disabled_bg": "#cb6e61",
      "selected_bg": "#fb0091",
      "dark_bg": "#fb8691",
      "disabled_dark_bg": "#db6671",
      "normal_text": "#202020",
      "hovered_text": "#303030",
      "selected_text": "#404040",
      "disabled_text": "#000000",
      "link_text": "#0000EE",
      "link_hover": "#2020FF",
      "link_selected": "#551A8B",
      "text_shadow": "#777777",
      "normal_border": "#ffB2A5",
      "hovered_border": "#ffC2B5",
      "disabled_border": "#Df9285",
      "selected_border": "#ff00A1"
    },
    "misc": {
      "state_transitions": {
        "normal_hovered": "0.1",
        "hovered_normal": "0.3"
      }
    }
  },
  "button": {
    "colours": {
      "normal_border": "#ffB2A5",
      "normal_text": "#FFFFFF"
    },
    "misc": {
      "shape": "rounded_rectangle",
      "shape_corner_radius": "18",
      "shadow_width": "2",
      "border_width": "1"
    }
  },
  "check_box": {
    "misc": {
      "shape": "ellipse",
      "shape_corner_radius": "3",
      "border_width": "2",
      "shadow_width": "2",
      "border_overlap": "1",
      "check_symbol": "",
      "indeterminate_symbol": "",
      "text_offset": "8",
      "tool_tip_delay": "1.5"
    },
    "images": {
      "selected_images": [
        {
          "id": "checked_image",
          "path": checkSVGpath,
          "layer": "0"
        }
      ]
    }
  },
  "#NoBorder": {
    "colours": {
      "normal_bg": "#FFF0",
      "hovered_bg": "#FFF0",
      "disabled_bg": "#FFF0",
      "selected_bg": "#FFF0",
      "dark_bg": "#FFF0"
    },
    "misc": {
      "border_width": "0",
      "shadow_width": "0"
    }
  }
}

file, THEMEPATH = tempfile.mkstemp('.json', text=True)
os.write(file, json.dumps(jsonTheme).encode())
os.close(file)


def cleanup():
    os.remove(THEMEPATH)


atexit.register(cleanup)
