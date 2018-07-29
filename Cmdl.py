from Card import *
import WistGame

class CmdLine:
    """ main command line"""
    in_str = None  #type: String
    wist_game = None #type: WistGame

    def __init__(self, wist_game):
        self.wist_game = wist_game
        pass

    def read_console(self):
        self.in_str = input('')
        return self.exec_line()

    def exec_line(self):
        """return nothing if there is an error"""
        try:
            cmd_obj = Cmd(self.in_str)
            return cmd_obj.execute(self.wist_game, self)
        except (ValueError,TypeError) as e:
            self.print_console(e)

    def print_array(self, array):
        str_to_print = ' '.join(array)
        self.print_console(str_to_print)

    def print_console(self, string):
        print(string)
        pass


class Cmd:
    """Cmd structure is command name and then arguments, seprated by spaces.
    sub class must set CMD_NAME attribute

    must be aware of the game instance
    """
    raw_cmd = None  # type: String
    cmd = None  # type: String
    cmd_args = None  # type: [String]
    COMMAND_LOCATION = 0
    CMD_NAME = None  # type: String
    sub_cmd_obj = None  # type:  child(Cmd)

    def __init__(self, raw_str):
        self.raw_cmd = raw_str
        self.parse_cmd()

    def execute(self, wist_game, cmd_line):
        if self.is_cmd_exist():
            if "execute" in dir(self.sub_cmd_obj):
                self.sub_cmd_obj.cmd_args = self.cmd_args
                return self.sub_cmd_obj.execute(wist_game, cmd_line)
            else:
                raise NotImplementedError("Execute not implemented in sub class")

        else:
            raise ValueError("Command " + self.cmd + " does not exist")

    def parse_cmd(self):
        """parse raw string cmd if nothing is enterd return Value Error"""
        parsed = self.raw_cmd.split(' ')
        final_parsed = []
        for word in parsed:
            if word != '':
                final_parsed.append(word)
        try:
            self.cmd = final_parsed[self.COMMAND_LOCATION]
            self.cmd_args = final_parsed[self.COMMAND_LOCATION + 1:]
        except IndexError:
            raise ValueError

    def is_cmd_exist(self):
        """ if command exist it returns the cammand class, else it returns 0"""
        sub_cmd_names = [sub_cmd.CMD_NAME for sub_cmd in type(self).__subclasses__()]
        #print(Cmd.__subclasses__())
        if self.cmd in sub_cmd_names:
            self.sub_cmd_obj = type(self).__subclasses__()[sub_cmd_names.index(self.cmd)]()
            return True
        else:
            return False


