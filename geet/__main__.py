import cmd
import os
import os.path
import sys
import signal
import traceback
from geet import core
from geet import about
from geet import handlers
import tkinter as tk
from tkinter import filedialog


# decorator for all commands handlers
def guard(func):
    def obj(self, arg):
        try:
            func(self, core.split_arg(arg))
        except Exception as e:
            print("Oops... Exception occurred !")
            print("".join(traceback.format_exception(*sys.exc_info())))
    return obj


class GeetManager(cmd.Cmd):
    intro = ("""Welcome to Geet !\n"""
             + """(v{})\n""".format(about.VERSION)
             + """Type "help" or "?" to list commands. Type "exit" to leave.\n""")

    prompt = "(geet) "

    def __init__(self):
        super().__init__()
        self.__gurl = core.get_gurl()

    @property
    def gurl(self):
        return self.__gurl

    # ===============================
    #           OVERRIDING
    # ===============================
    def preloop(self):
        pass

    def precmd(self, line):
        if line == "EOF":
            line = ""
        print("")
        return line

    def postcmd(self, stop, line):
        print("")
        return stop

    def emptyline(self):
        pass

    @guard
    def default(self, args):
        handlers.default_handler(args, self.gurl)
        return None

    # ===============================
    #            COMMANDS
    # ===============================
    @guard
    def do_rate(self, args):
        handlers.rate_handler(args, self.gurl)


    @guard
    def do_auth(self, args):
        handlers.auth_handler(args, self.gurl)

    @guard
    def do_install(self, args):
        handlers.install_handler(args, self.gurl)

    @guard
    def do_rollback(self, args):
        handlers.rollback_handler(args, self.gurl)

    @guard
    def do_list(self, args):
        handlers.list_handler(args, self.gurl)

    @guard
    def do_del(self, args):
        handlers.del_handler(args, self.gurl)

    @guard
    def do_run(self, args):
        handlers.run_handler(args, self.gurl)

    @guard
    def do_version(self, args):
        handlers.version_handler(args, self.gurl)

    @guard
    def do_path(self, args):
        handlers.path_handler(args, self.gurl)

    @guard
    def do_exit(self, args):
        print("Exiting...")
        sys.exit()

    # ===============================
    #            COMMANDS
    # ===============================
    def help_rate(self):
        print(handlers.rate_handler.__doc__)

    def help_auth(self):
        print(handlers.auth_handler.__doc__)

    def help_install(self):
        print(handlers.install_handler.__doc__)

    def help_rollback(self):
        print(handlers.rollback_handler.__doc__)

    def help_list(self):
        print(handlers.list_handler.__doc__)

    def help_del(self):
        print(handlers.del_handler.__doc__)

    def help_run(self):
        print(handlers.run_handler.__doc__)

    def help_version(self):
        print("Help")

    def help_path(self):
        print(handlers.path_handler.__doc__)

    def help_exit(self):
        print("Exit")


def signal_handler(signum, frame, pm):
    pm.do_exit([])
    return


def check_init():
    if not core.should_init_geet():
        return True
    print("")
    print("  Oops ! Geet hasn't been fully initialized !")
    print("")
    print("  Geet needs a folder to install apps inside.")
    print("  It doesn't have to be an empty directory.")
    print("  Enter a path or press Enter to launch a file dialog.")
    dest = input("  Directory: ")
    if dest == "":
        dest = open_folder_chooser()
        if dest is None:
            print("  Cancelled")
            return False
        print("  {}".format(dest))
    if not os.path.exists(dest):
        print("  This path doesn't exist")
        print("  Cancelled")
        return False
    # init
    data = core.init_geet(dest)
    error_code = data["error_code"]
    if error_code == 0:
        print("  Successfully initialized")
        print("\n")
        return True
    elif error_code == 1:
        print("  Failed to create 'got-with-geet' folder")
        return False
    elif error_code == 2:
        print("  Failed to register Geet in $HOME/PyrusticData")
        return False
    else:
        raise Exception("Unknown error code")


def open_folder_chooser():
    initialdir = os.path.abspath(os.sep)
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(initialdir=initialdir,
                                   title="Select your a directory")
    root.destroy()
    if not isinstance(path, str) or not path:
        return
    return path


# ===============================
#
# ===============================

# Check init then init Geet if needed
try:
    is_success = check_init()
    if not is_success:
        print("")
        exit(0)
except KeyboardInterrupt:
    print("")
    exit(0)
#
if len(sys.argv) == 1:
    gm = GeetManager()
    signal.signal(signal.SIGINT,
                  lambda signum, frame, gm=gm: signal_handler(signum, frame, gm))
    try:
        gm.cmdloop()
    except KeyboardInterrupt:
        pass
else:
    command = sys.argv[1].lower()
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    legal_commands = ["rate", "install",
                      "rollback", "list",
                      "run", "path",
                      "del", "version"]
    handlers_funcs = [handlers.rate_handler, handlers.install_handler,
                      handlers.rollback_handler, handlers.list_handler,
                      handlers.run_handler, handlers.path_handler,
                      handlers.del_handler, handlers.version_handler]
    handler_to_call = handlers.default_handler
    if command in legal_commands:
        index = legal_commands.index(command)
        handler_to_call = handlers_funcs[index]
    else:
        handler_to_call = handlers.default_handler
        args = [command]
    # call
    gurl = core.get_gurl()
    try:
        handler_to_call(args, gurl)
        print("\n  Exiting...")
    except KeyboardInterrupt:
        print("\n  Exiting...")
        sys.exit(0)
