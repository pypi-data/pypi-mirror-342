class BaseError(Exception):
    """
    Base exception.
    """

    def __init__(self, message, stacktrace = None):
        self.message = message
        self.stacktrace = stacktrace

    def __str__(self):
        exception_message = ""
        if self.message:
            exception_message += "%s" % self.message
        return exception_message


class ArgumentError(BaseError):
    """
    The arguments passed to an operation are either invalid or malformed.
    """
    pass


class ArgumentNullError(ArgumentError):
    """
    The arguments passed to an operation are null.
    """
    pass


class ArgumentOutOfRangeError(ArgumentError):
    """
    The arguments passed to an operation are out of range.
    """
    pass

class NotSupportedError(BaseError):
    pass


class NotSupportedOperationError(NotSupportedError):

    def __init__(self, automation_tech, control_type, operation, message, stacktrace = None):
        self.automation_tech = automation_tech
        self.control_type = control_type
        self.operation = operation
        super(NotSupportedOperationError, self).__init__(message, stacktrace)    


class NotSupportedOperationOptionError(NotSupportedOperationError):
    def __init__(self, automation_tech, control_type, operation, option, message, stacktrace = None):
        self.option = option
        super(NotSupportedOperationOptionError, self).__init__(automation_tech, control_type, operation, message, stacktrace)


class InvalidOperationError(BaseError):
    pass


class InvalidSelectedItemError(InvalidOperationError):
    def __init__(self, item, message, stacktrace = None):
        self.item = item
        super(InvalidSelectedItemError, self).__init__(message, stacktrace)


class OperationTimeoutError(BaseError):
    pass


class ElementNotFoundError(BaseError):
    pass


class WindowError(BaseError):
    pass


class WindowsNativeError(WindowError):
    def __init__(self, name, native_errorcode, message, stacktrace = None):
        self.name = name
        self.native_errorcode = native_errorcode
        super(WindowsNativeError, self).__init__(message, stacktrace)


class UiaPatternNotFoundError(WindowError):
    def __init__(self, message, stacktrace = None):
        super(UiaPatternNotFoundError, self).__init__(message, stacktrace)


class ScreenOperationError(WindowsNativeError):
    def __init__(self, name, native_errorcode, message, stacktrace = None):
        super(ScreenOperationError, self).__init__(name, native_errorcode, message, stacktrace)


class WebError(BaseError):
    def __init__(self, browser_type, message, stacktrace = None):
        self.browser_type = browser_type
        super(WebError, self).__init__(message, stacktrace)


class BrowserNotRunError(WebError):
    def __init__(self, browser_type, message, stacktrace = None):
        super(BrowserNotRunError, self).__init__(browser_type, message, stacktrace)


class BrowserNotInstallError(WebError):
    def __init__(self, browser_type, message, stacktrace = None):
        super(BrowserNotInstallError, self).__init__(browser_type, message, stacktrace)


class UnreachableBrowserExtensionError(WebError):
    def __init__(self, browser_type, message, stacktrace = None):
        super(UnreachableBrowserExtensionError, self).__init__(browser_type, message, stacktrace)


class WebElementNotRespondingError(WebError):
    def __init__(self, browser_type, message, stacktrace = None):
        super(WebElementNotRespondingError, self).__init__(browser_type, message, stacktrace)

class ChromiumNotSupportError(WebError):
    def __init__(self, browser_type, message, stacktrace = None):
        super(ChromiumNotSupportError, self).__init__(browser_type, message, stacktrace)

class LocatorUndefinedError(BaseError):
    pass

class ProjectSettingNotFoundError(BaseError):
    pass

class UnAuthorizedError(BaseError):
    pass

class LocatorRequestError(BaseError):
    pass

class ExtensionOperationError(BaseError):
    def __init__(self, operation, extention_type, message):
        self.operation = operation
        self.extention_type = extention_type
        super(ExtensionOperationError, self).__init__(message)