class customError(Exception):
    def __init__(self, *args):

        if args.__len__() > 1:
            self.title = args[0]
            self.message = args[1]

        else:
            print(args)
            self.title = args[0]
            self.message = None

    def __str__(self):
        if self.message:
            return f"{self.title}: {self.message}"
        else:
            return f"{self.title}"
