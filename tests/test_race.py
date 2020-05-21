from easyprocess import EasyProcess
from pyvirtualdisplay import Display
import sys
from entrypoint2 import entrypoint
from time import sleep
from pyvirtualdisplay.util import get_helptext
from tutil import platform_is_osx

# ubuntu 14.04 no displayfd
# ubuntu 16.04 displayfd
# ubuntu 18.04 displayfd


def has_displayfd():
    return "-displayfd" in get_helptext("Xvfb")


# TODO:remove
if has_displayfd():
    # TODO: osx error:            Cannot open "/tmp/server-0.xkm" to write keyboard description
    if not platform_is_osx():

        def test_race_10():
            check_N(10)


def check_N(N):
    ls = []
    try:
        for i in range(N):
            cmd = [
                sys.executable,
                __file__.rsplit(".", 1)[0] + ".py",
                str(i),
                "--debug",
            ]
            p = EasyProcess(cmd)
            p.start()
            ls += [p]

        sleep(3)

        good_count = 0
        for p in ls:
            p.wait()
            if p.return_code == 0:
                good_count += 1
    finally:
        for p in ls:
            p.stop()
    print(good_count)
    assert good_count == N


@entrypoint
def main(i):
    # TODO: test all backends
    d = Display().start()
    print("my index:%s  disp:%s" % (i, d.new_display_var))
    ok = d.is_alive()
    d.stop()
    assert ok
