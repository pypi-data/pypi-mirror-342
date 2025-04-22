class _Constants:

    SdkVersion = "0.2.5"
    LocatorFolder = ".locator"
    ClickniumYaml = "clicknium.yaml"

    EventDataMethodKey = "Method"
    EventDataMessageKey = "Message"
    EventDataStacktraceKey = "Stacktrace"
    
    InvalidColor="Invalid color. The valid value is between '#000000' ~ '#ffffff'."
    FilePathInvalidError = "File path %s is invalid."
    LocatorNotExist="Can not find the locator: %s."
    ProjectSettingNotFound = "Can not find project settings file 'clicknium.yaml'."
    BrowserNotInstalled = "%s extension %s failed. %s browser is not installed."
    BrowserVersionNotSupported = "%s extension %s failed. %s browser's version is not supported."
    BrowserOperationEnd = "%s %s extension finished. Make sure you have turned on this extension in %s browser."
    ExtensionInstallerIsRunning = "%s extension %s failed. The installer program is already running."
    ExtensionOperationCancelled = "%s extension %s has been cancelled."
    ExtensionOpearationFailed = "%s extension %s failed."
    ExtensionOperationStart = "Start to %s %s extension..."
    ExtensionDetectOperationStart = "Start to detect %s extension installation status..."
    ExtensionDetectStatusUnknown = "Detect %s extension installation status failed with unknown issue."
    ExtensionDetectStatusUninstalled = "%s extension has not been installed yet."
    ExtensionDetectStatusInstalled = "%s extension has been installed with latest version."
    ExtensionDetectStatusNeedUpdate = "%s extension has been installed and there is an update available to update."
    JavaScanFolder = "Try scanning java installation folder under %s."
    JavaExtensionEnd = "Java extension %s finished."
    JavaExtensionFailed = "Java extension %s failed."

    TelemetryBlanklist = ["find_element", "get_webdriver", "get_windowdriver", "get_sapdriver", "get_mousedriver"]

class _ExceptionNames:

    ArgumentException = "ArgumentException"
    ArgumentNullException = "ArgumentNullException"
    ArgumentOutOfRangeException = "ArgumentOutOfRangeException"

    NotSupportedException = "NotSupportedException"
    OperationNotSupportedException = "OperationNotSupportedException"
    OperationOptionNotSupportedException = "OperationOptionNotSupportedException"

    InvalidOperationException = "InvalidOperationException"
    InvalidSelectedItemException = "InvalidSelectedItemException"

    TimeoutException = "TimeoutException"

    WindowsNativeException = "WindowsNativeException"
    UiaPatternNotFoundException = "UiaPatternNotFoundException"
    ScreenOperationException = "ScreenOperationException"

    BrowserNotRunException = "BrowserNotRunException"
    BrowserNotInstallException = "BrowserNotInstallException"
    UnreachableBrowserExtensionException = "UnreachableBrowserExtensionException"
    WebElementNotRespondingException = "WebElementNotRespondingException"
    ChromiumNotSupportException = "ChromiumNotSupportException"
    