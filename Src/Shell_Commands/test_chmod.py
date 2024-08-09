import re
import ESXi_fs as fs
import ESXi_command as cmd

MODE_REGEX = r"^[ugoa]*([-+=]([rwxXst]*|[ugo]))+|[-+=]?[0-7]+$"

class ESXiChmodCommand(cmd.SimpleCommand):
    """/bin/chmod"""
    def run(self):
        if "--help" in self.args or "-h" in self.args:
            self.show_help()
            return

        # arguments
        opts, mode, files, error = self.parse_args()
        if error:
            return

        # mode
        if not re.fullmatch(MODE_REGEX, mode):
            self.stderr = f"chmod: invalid mode: '{mode}'"
            self.returncode = 1
            return

        # handle files
        for file in files:
            path = self.fs.resolve_path(file)
            try:
                # Change Mode (Emulate)
                if self.fs.isfile(path) or self.fs.isdir(path):
                    self.stdout += f"Mode of '{file}' changed.\n"
                else:
                    self.stderr += f"chmod: cannot access '{file}': No such file or directory\n"
                    self.returncode = 1
            except PermissionError:
                self.stderr += f"chmod: changing permissions of '{file}': Operation not permitted\n"
                self.returncode = 1

    def parse_args(self):
        """
        Analyze arguments
        """
        mode = None
        opts = []
        files = []
        error = False

        # check mode
        for i, arg in enumerate(self.args):
            if re.fullmatch(MODE_REGEX, arg):
                mode = arg
                del self.args[i]
                break

        # option
        for arg in self.args:
            if arg.startswith("-"):
                opts.append(arg)
            else:
                files.append(arg)

        # error
        if not mode:
            self.stderr = "chmod: missing operand"
            error = True
        elif not files:
            self.stderr = f"chmod: missing operand after '{mode}'"
            error = True

        return opts, mode, files, error

    def show_help(self):
        self.write_output(
            """Usage: chmod [-Rcvf] MODE[,MODE]... FILE...

Each MODE is one or more of the letters ugoa, one of the
symbols +-= and one or more of the letters rwxst

        -R      Recurse
        -c      List changed files
        -v      List all files
        -f      Hide errors
"""
)