import logging

from easyprocess import EasyProcess

from pyvirtualdisplay.abstractdisplay import AbstractDisplay

log = logging.getLogger(__name__)

PROGRAM = "Xvfb"


class XvfbDisplay(AbstractDisplay):
    """
    Xvfb wrapper

    Xvfb is an X server that can run on machines with no display
    hardware and no physical input devices. It emulates a dumb
    framebuffer using virtual memory.
    """

    def __init__(
        self,
        size=(1024, 768),
        color_depth=24,
        bgcolor="black",
        use_xauth=False,
        check_startup=False,
        fbdir=None,
        dpi=None,
        randomizer=None,
    ):
        """
        :param bgcolor: 'black' or 'white'
        :param fbdir: If non-null, the virtual screen is memory-mapped
            to a file in the given directory ('-fbdir' option)
        :param dpi: screen resolution in dots per inch if not None
        """
        self.screen = 0
        self.size = size
        self.color_depth = color_depth
        self.process = None
        self.bgcolor = bgcolor
        self.display = None
        self.fbdir = fbdir
        self.dpi = dpi

        p = EasyProcess([PROGRAM, "-help"])
        p.enable_stdout_log = False
        p.enable_stderr_log = False
        p.call()
        helptext = p.stdout
        self.has_displayfd = "-displayfd" in helptext

        AbstractDisplay.__init__(
            self,
            use_xauth=use_xauth,
            check_startup=check_startup,
            randomizer=randomizer,
        )

    def _cmd(self):
        cmd = [
            dict(black="-br", white="-wr")[self.bgcolor],
            "-nolisten",
            "tcp",
            "-screen",
            str(self.screen),
            "x".join(map(str, list(self.size) + [self.color_depth])),
            self.new_display_var,
        ]
        if self.fbdir:
            cmd += ["-fbdir", self.fbdir]
        if self.dpi is not None:
            cmd += ["-dpi", str(self.dpi)]
        if self.check_startup:
            if self.has_displayfd:
                cmd += ["-displayfd", str(self.check_startup_fd)]
        return [PROGRAM] + cmd
