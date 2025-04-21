import enum


class ApplicationRuntimeState(int, enum.Enum):
    BOOTING         = 0
    STARTUP         = 1
    LIVE            = 2
    READY           = 3
    BUSY            = 4
    TEARDOWN        = -1
    BOOTFAILURE     = -2
    RELOADFAILURE   = -3
    FATAL           = -99