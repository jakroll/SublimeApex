import sublime
from .salesforce import message
from . import util

class ThreadProgress():
    """
    Stolen from Package Control Source Code, ni dong de
    
    Animates an indicator, [=   ], in the status area while a thread runs

    :param thread:
        The thread to track for activity

    :param message:
        The message to display next to the activity indicator

    :param success_message:
        The message to display once the thread is complete
    """

    def __init__(self, api, thread, message, success_message, open_console=True):
        self.api = api
        self.thread = thread
        self.message = message
        self.success_message = success_message
        self.addend = 1
        self.size = 15
        self.open_console = open_console
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if not self.thread.is_alive():
            if hasattr(self.thread, 'result') and not self.thread.result:
                sublime.status_message('')
                return

            # Invoked in update.py
            if self.api == None: return

            # If result is None, it means timeout
            if self.api.result == None: 
                sublime.error_message("Request timeout, please check your network access")
                return

            # After thread is end, display feedback to end user
            # according to response
            result = self.api.result
            if isinstance(result, dict) and\
                (("status_code" in result and result["status_code"] > 399) or\
                 ("success" in result and not result["success"])):
                
                print (message.SEPRATE.format(util.format_error_message(result)))
                if self.open_console:
                    sublime.active_window().run_command("show_panel", 
                        {"panel": "console", "toggle": False})
            else:
                sublime.status_message(self.success_message)
            return

        before = i % self.size
        after = (self.size - 1) - before

        sublime.status_message('%s [%s=%s]' % \
            (self.message, ' ' * before, ' ' * after))

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend

        sublime.set_timeout(lambda: self.run(i), 100)

class ThreadsProgress():
    """
    Stolen from Package Control Source Code, ni dong de
    
    Animates an indicator, [=       ], in the status area while a thread runs

    :param threads:
        The threads to track for activity

    :param message:
        The message to display next to the activity indicator

    :param success_message:
        The message to display once the thread is complete
    """

    def __init__(self, threads, message, success_message):
        self.threads = threads
        self.message = message
        self.success_message = success_message
        self.addend = 1
        self.size = 15
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if self.is_threads_end(self.threads):
            sublime.status_message(self.success_message)
            return

        before = i % self.size
        after = (self.size - 1) - before

        sublime.status_message('%s [%s=%s]' % \
            (self.message, ' ' * before, ' ' * after))

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend

        sublime.set_timeout(lambda: self.run(i), 100)

    def is_threads_end(self, threads):
        """
        Indicate whether all threads are end

        @threads: Threads
        @return: Bool
        """

        is_alive = True
        for thread in threads:
            if thread.is_alive(): is_alive = False

        return is_alive