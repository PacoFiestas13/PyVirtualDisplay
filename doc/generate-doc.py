import logging
import os

from easyprocess import EasyProcess
from entrypoint2 import entrypoint

from pyvirtualdisplay.smartdisplay import SmartDisplay

# (cmd,grab,background)
commands = [
    ("python3 -m pyvirtualdisplay.examples.screenshot", False, False),
    ("python3 -m pyvirtualdisplay.examples.lowres", True, False),
    ("python3 -m pyvirtualdisplay.examples.nested", True, False),
    ("python3 -m pyvirtualdisplay.examples.vncserver", False, True),
    ("vncviewer localhost:5904", True, True),
]


def screenshot(cmd, fname):
    logging.info("%s %s", cmd, fname)
    # fpath = "docs/_img/%s" % fname
    # if os.path.exists(fpath):
    #     os.remove(fpath)
    with SmartDisplay() as disp:
        with EasyProcess(cmd):
            img = disp.waitgrab()
            img.save(fname)


@entrypoint
def main():
    pls = []
    try:
        os.chdir("gen")
        for cmd, grab, bg in commands:
            with SmartDisplay() as disp:
                logging.info("cmd: %s", cmd)
                fname_base = cmd.replace(" ", "_")
                fname = fname_base + ".txt"
                logging.info("cmd: %s", cmd)
                print("file name: %s" % fname)
                with open(fname, "w") as f:
                    f.write("$ " + cmd)
                    if bg:
                        p = EasyProcess(cmd).start()
                    else:
                        p = EasyProcess(cmd).call()
                        f.write(p.stdout)
                        f.write(p.stderr)
                    pls += [p]
                if grab:
                    png = fname_base + ".png"
                    img = disp.waitgrab(timeout=3)
                    logging.info("saving %s", png)
                    img.save(png)
    finally:
        os.chdir("..")
        for p in pls:
            p.stop()
    embedme = EasyProcess(["npx", "embedme", "../README.md"])
    embedme.call()
    print(embedme.stdout)
    assert embedme.return_code == 0
    assert not "but file does not exist" in embedme.stdout
