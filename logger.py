import logging

class Logger():

    instance = None

    @staticmethod
    def getLogger():
        if Logger.instance == None:
            Logger.instance = Logger.__initLogger()
        return Logger.instance

    @classmethod
    def __initLogger(cls):
        loggerFmt = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.DEBUG)
        logHandler = logging.StreamHandler()
        logHandler.setFormatter(loggerFmt)
        rootLogger.addHandler(logHandler)
        return rootLogger