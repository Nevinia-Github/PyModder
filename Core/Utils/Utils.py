import os


def notnone(t):
    return t if t is not None else ""


def save_template(file, template, replaces):
    with open(os.path.join(os.path.dirname(__file__), "..", "Project", "Templates", template), "r") as f:
        text = f.read()
    for k, v in replaces.items():
        text = text.replace(k, v)
    with open(file, "w") as f:
        f.write(text)
