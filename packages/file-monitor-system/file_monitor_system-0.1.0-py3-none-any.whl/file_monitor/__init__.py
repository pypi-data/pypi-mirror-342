import platform

class FileMonitor:
    def __init__(self, path=".", alert_callback=None):
        self.path = path
        self.alert_callback = alert_callback

        if platform.system() == "Windows":
            from .watchers.windows_watcher import start_watch
        else:
            from .watchers.cross_platform_watcher import start_watch

        self._start_watch = start_watch

    def start(self):
        print(f"[INFO] Monitoring started on: {self.path}")
        self._start_watch(self.path, self.alert_callback)

    def stop(self):
        print("[INFO] Monitoring stopped.")
