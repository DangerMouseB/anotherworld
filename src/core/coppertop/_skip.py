# *******************************************************************************
#
#    Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# *******************************************************************************


import sys
if hasattr(sys, '_ImportTrace') and sys._ImportTrace: print(__name__)

# _Skipper was created to reduce the debugging noise when using @pipeable decorated
# functions - basically it skips any trace events that correspond to the pipeable
# implementation - adverbs can be switched on or off :)


import inspect, itertools, threading
from ._core import Missing, ProgrammerError, UnhappyWomble


# useful
# https://stackoverflow.com/questions/59088671/hooking-every-function-call-in-python
# https://explog.in/notes/settrace.html

# https://stackoverflow.com/questions/51752911/run-code-partially-in-debug-mode-in-pycharm
# https://stackoverflow.com/questions/42601684/tell-pycharm-debugger-to-not-enter-into-decorators

# https://www.pydev.org/history_pydev.html  - especially see 3.9.2 and 3.7.0
# https://github.com/JetBrains/intellij-community/tree/master/python/helpers/pydev
# https://blog.jetbrains.com/pycharm/2016/05/debugger-interview-with-pydev-and-pycharm/
# https://youtrack.jetbrains.com/issue/PY-40661

#https://stackoverflow.com/questions/15164565/debugging-with-pycharm-how-to-step-into-project-without-entering-django-librar/15186219#15186219
#https://youtrack.jetbrains.com/issue/PY-9101
#https://youtrack.jetbrains.com/issue/PY-9669
#https://intellij-support.jetbrains.com/hc/en-us/community/posts/206602815-Black-Boxing-Framework-Code

# Elizaveta Shashkova commented 8 Aug 2016 20:48
# The stepping filters have appeared in PyCharm 2016.1 (PY-18493)
#https://youtrack.jetbrains.com/issue/PY-18493

# https://github.com/fabioz/debugpy
# https://github.com/fabioz/watchgod
# https://github.com/fabioz/python-language-server
# https://github.com/fabioz/PyDev.Debugger/blob/a4a58179dab9f9fb93559066f0ef22ac59c59e04/_pydevd_bundle/pydevd_process_net_command.py


# could think about this more one day but for my uses we just need to
# handle pycharm (eclipse and vscode I believe also use pydev). Possibly
# need to handle WingPro
_debugger = 'pydev'





class _Skipper(object):
    # a singleton so could just as easily be a module
    logSeed = itertools.count(start=1)
    @classmethod
    def log(cls, t):
        sys._skipperLog.append((next(cls.logSeed),) + t)

    def __init__(s):
        s.chatty = False
        s.suppressAll = False
        s.otherMain = Missing
        s.skipFiles = ('_pipe.py', '_repl.py', '_skip.py', 'adverbs.py')


    def install(s):
        thisFrame = sys._getframe(0)
        callerFrame = thisFrame.f_back

        s.otherMain = sys.gettrace()
        traceFn = callerFrame.f_trace

        if traceFn and _debugger == 'pydev':
            # see http://pydev.blogspot.com/2007/06/why-cant-pydev-debugger-work-with.html
            try:
                import pydevd
                debugger = pydevd.GetGlobalDebugger()
                traceFn = debugger.trace_dispatch if debugger else None
            except ImportError:
                pass
        s.log(("installing", threading.current_thread().name, threading.get_ident()))
        sys.settrace(s.callFn)
        # callerFrame.f_trace = TraceFn(s, traceFn)
        s.log(("installed",))



    def uninstall(s):
        if sys.gettrace() == s.callFn:
            sys.settrace(s.otherMain)
            s.log(("uninstalled", threading.current_thread().name, threading.get_ident()))
        else:
            s.log(("can't uninstall", threading.current_thread().name, threading.get_ident()))



    def note(s, note):
        # if sys.gettrace() == s.callFn:
        s.log((note, threading.current_thread().name, threading.get_ident()))
        # else:
        #     raise UnhappyWomble()



    def callFn(s, frame, event, arg):
        1/0
        sys._skipperFn = frame.f_code.co_name
        if s.suppressAll: return None

        filename = frame.f_code.co_filename.split('/')[-1]
        skip = (filename in s.skipFiles)

        if skip:
            # if s.chatty:
            #     s.log((event + ' - skip', frame.f_code.co_name, frame.f_lineno, filename))
            #     if frame.f_code.co_name in ('__rrshift__', '__call__', '__rshift'):
            #         s.log(('co_names', frame.f_code.co_names))
            #         s.log(('co_freevars', frame.f_code.co_freevars))
            #         s.log(('co_consts', frame.f_code.co_consts))
            #         s.log(('co_varnames', frame.f_code.co_varnames))
            #frame.f_trace = TraceFn(s, Missing)
            shouldTrace = "ENT" in frame.f_code.co_consts
            if not shouldTrace:
                if s.chatty:
                    s.log((event + ' - skip', frame.f_code.co_name, frame.f_lineno, filename))
                frame.f_trace = TraceFn(s, Missing)
                return frame.f_trace
        else:
            if s.chatty: s.log((event, frame.f_code.co_name, frame.f_lineno, filename))

        # PASS CONTROL TO OTHER
        if s.chatty: s.log((frame.f_code.co_name, "MAIN", frame.f_trace))
        sys._skipperFrame = sys._getframe(0)
        traceFn = s.otherMain(frame, event, arg)
        if sys.gettrace() != s.callFn:
            raise UnhappyWomble()
        if traceFn:
            frame.f_trace = TraceFn(s, traceFn)
            if s.chatty: s.log((frame.f_code.co_name, "        TRACE", frame.f_trace.id, id(frame.f_trace.otherFn)))
            return frame.f_trace
        else:
            if s.chatty: s.log((frame.f_code.co_name, "        DONE"))
            return None



class TraceFn(object):
    idSeed = itertools.count(start=1)

    def __init__(tf, skipper, otherFn):
        tf.skipper = skipper
        tf.otherFn = otherFn
        tf.id = next(tf.idSeed)



    def __call__(tf, frame, event, arg):
        1/0
        sys._skipperTrace = tf.id
        skipper = tf.skipper
        filename = frame.f_code.co_filename.split('/')[-1]

        if event == 'line':
            skip = (filename in skipper.skipFiles)
            if skip:
                shouldTrace = "ENT" in frame.f_code.co_consts
                if skipper.chatty:
                    skipper.log((event + ' - skip', frame.f_code.co_name, frame.f_lineno, filename))
                    # if shouldTrace:
                    #     skipper.log(('co_names', frame.f_code.co_names))
                    #     skipper.log(('co_freevars', frame.f_code.co_freevars))
                    #     skipper.log(('co_consts', frame.f_code.co_consts))
                    #     skipper.log(('co_varnames', frame.f_code.co_varnames))
                frame.f_trace_lines = False    # suppress line events but keep return events
                #if not shouldTrace:
                # return tf

        elif event == 'return':
            callerFrame = frame.f_back
            callerFilename = callerFrame.f_code.co_filename.split('/')[-1]
            if filename in skipper.skipFiles:
                if skipper.chatty:
                    skipper.log((event + ' - skip1', frame.f_code.co_name, frame.f_lineno, filename))
                    skipper.log((event + ' - skip1', callerFrame.f_code.co_name, callerFrame.f_lineno, callerFilename))
                # return tf.returnFn
            if (callerFilename in skipper.skipFiles):
                if skipper.chatty:
                    skipper.log((event + ' - skip2', frame.f_code.co_name, frame.f_lineno, filename))
                    skipper.log((event + ' - skip2', callerFrame.f_code.co_name, callerFrame.f_lineno, callerFilename))
                # return tf.returnFn

        elif event == 'exception':
            skip = (filename in skipper.skipFiles)  # (frame.f_code.co_name not in ('__rrshift__',))
            if skip:
                if skipper.chatty: skipper.log((event + ' - skip', frame.f_code.co_name, frame.f_lineno, filename))
                return tf

        elif event == 'opcode':
            raise ProgrammerError('opcode should not be enabled for this frame')

        else:
            raise ProgrammerError()

        if tf.otherFn is Missing:
            skipper.log((event + ' - totalSkip', frame.f_code.co_name, frame.f_lineno, filename))
            if not sys.gettrace() == skipper.callFn:
                skipper.log((event, "CALLFN HIJACKED"))
                sys.settrace(skipper.callFn)
            return tf
        if tf.otherFn is None:
            skipper.log((event + ' - None', frame.f_code.co_name, frame.f_lineno, filename))
            return tf

        # PASS CONTROL TO OTHER - MAY BLOCK IN UI
        if skipper.chatty: skipper.log((event, "TRACE", frame.f_code.co_name, frame.f_lineno, filename, frame.f_trace.id, id(frame.f_trace.otherFn)))
        sys._skipperFrame = sys._getframe(0)
        tf.otherFn = tf.otherFn(frame, event, arg)
        if not sys.gettrace() == skipper.callFn:
            skipper.log((event, "CALLFN HIJACKED"))
            sys.settrace(skipper.callFn)
        if frame.f_trace is not None and not isinstance(frame.f_trace, TraceFn):
            skipper.log((event, "TRACEFN CHANGED"))
            skipper.log((event, "        GOT", id(frame.f_trace), frame.f_trace))
            skipper.log((event, "        EXPECTING", id(tf.otherFn), tf.otherFn))
            frame.f_trace = TraceFn(skipper, tf)
        if event == 'line':
            if tf.otherFn:
                if skipper.chatty: skipper.log((event, "        TRACE1", frame.f_code.co_name, frame.f_lineno, filename, frame.f_trace.id, id(frame.f_trace.otherFn)))
                return tf
            else:
                if skipper.chatty: skipper.log((event, "        DONE", frame.f_code.co_name, frame.f_lineno, filename, frame.f_trace.id, id(frame.f_trace.otherFn)))
                return None
        elif event == 'return':
            if tf.otherFn:
                if skipper.chatty: skipper.log((event, "        TRACE2", frame.f_code.co_name, frame.f_lineno, filename, frame.f_trace.id, id(frame.f_trace.otherFn)))
                return tf.otherFn
            else:
                if skipper.chatty: skipper.log((event, "        DONE", frame.f_code.co_name, frame.f_lineno, filename, frame.f_trace.id, id(frame.f_trace.otherFn)))
                return None
        elif event == 'exception':
            if tf.otherFn:
                if skipper.chatty: skipper.log((event, "        TRACE3", frame.f_code.co_name, frame.f_lineno, filename, frame.f_trace.id, id(frame.f_trace.otherFn)))
                return tf.otherFn
            else:
                if skipper.chatty: skipper.log((event, "        DONE", frame.f_code.co_name, frame.f_lineno, filename, frame.f_trace.id, id(frame.f_trace.otherFn)))
                return None
        elif event == 'opcode':
            if tf.otherFn:
                if skipper.chatty: skipper.log((event, "        TRACE4", frame.f_code.co_name, frame.f_lineno, filename, frame.f_trace.id, id(frame.f_trace.otherFn)))
                return tf.otherFn
            else:
                if skipper.chatty: skipper.log((event, "        DONE", frame.f_code.co_name, frame.f_lineno, filename, frame.f_trace.id, id(frame.f_trace.otherFn)))
                return None
        else:
            raise ProgrammerError()

    def returnFn(s, frame, event, arg):
        raise UnhappyWomble('reread - https://docs.python.org/3/library/sys.html#sys.settrace')


# class Unhijacker(object):
#     def __init__(self, skipper, frame, tf):
#         self.skipper = skipper
#         self.frame = frame
#         self.tf = tf
#     def __call__(self, frame, event, arg):
#         answer = self.tf.otherFn(frame, event, arg)
#         self.skipper.log((event, "UN HIJACKED"))
#         sys.settrace(self.skipper.callFn)
#         frame.f_trace = self.tf




_gi = _Skipper()
sys._skipperLog = []
try:
    import pydevd
    sys._debugger = pydevd.GetGlobalDebugger()
except:
    pass

# debugger = get_global_debugger()
#
# debugger.set_trace_for_frame_and_parents(get_frame().f_back)
#
# t = threadingCurrentThread()
# additional_info = set_additional_thread_info(t)
#
# debugger.enable_tracing()


x = ['SetTrace',
 '__class__',
 '__delattr__',
 '__dict__',
 '__dir__',
 '__doc__',
 '__eq__',
 '__format__',
 '__ge__',
 '__getattribute__',
 '__gt__',
 '__hash__',
 '__init__',
 '__init_subclass__',
 '__le__',
 '__lt__',
 '__module__',
 '__ne__',
 '__new__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__setattr__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 '__weakref__',
 '_activate_mpl_if_needed',
 '_call_mpl_hook',
 '_cmd_queue',
 '_create_check_output_thread',
 '_create_pydb_command_thread',
 '_do_wait_suspend',
 '_exec',
 '§',
 '_finish_debugging_session',
 '_local_thread_trace_func',
 '_lock_running_thread_ids',
 '_main_lock',
 '_mark_suspend',
 '_py_db_command_thread_event',
 '_running_thread_ids',
 '_send_breakpoint_condition_exception',
 '_set_breakpoints_with_id',
 '_termination_event_set',
 '_threads_suspended_single_notification',
 'add_break_on_exception',
 'asyncio_analyser',
 'break_on_caught_exceptions',
 'break_on_uncaught_exceptions',
 'breakpoints',
 'cancel_async_evaluation',
 'check_output_redirect',
 'clear_skip_caches',
 'cmd_factory',
 'collect_return_info',
 'communication_role',
 'connect',
 'consolidate_breakpoints',
 'disable_property_deleter_trace',
 'disable_property_getter_trace',
 'disable_property_setter_trace',
 'disable_property_trace',
 'disable_tracing',
 'do_wait_suspend',
 'dummy_trace_dispatch',
 'enable_output_redirection',
 'enable_tracing',
 'exiting',
 'file_to_id_to_line_breakpoint',
 'file_to_id_to_plugin_breakpoint',
 'filename_to_lines_where_exceptions_are_ignored',
 'finish_debugging_session',
 'first_breakpoint_reached',
 'frame_eval_func',
 'get_internal_queue',
 'get_plugin_lazy_init',
 'get_thread_local_trace_func',
 'has_plugin_exception_breaks',
 'has_plugin_line_breaks',
 'has_threads_alive',
 'ignore_exceptions_thrown_in_lines_with_ignore_exception',
 'in_project_scope',
 'init_matplotlib_in_debug_console',
 'init_matplotlib_support',
 'initialize_network',
 'is_exception_trace_in_project_scope',
 'is_filter_enabled',
 'is_filter_libraries',
 'is_ignored_by_filters',
 'is_test_item_or_set_up_caller',
 'is_top_level_trace_in_project_scope',
 'mpl_hooks_in_debug_console',
 'mpl_in_use',
 'mpl_modules_for_patching',
 'mtime',
 'multi_threads_single_notification',
 'notify_thread_created',
 'notify_thread_not_alive',
 'on_breakpoints_changed',
 'output_checker_thread',
 'patch_threads',
 'plugin',
 'post_internal_command',
 'prepare_to_run',
 'process_created_msg_received_events',
 'process_internal_commands',
 'py_db_command_thread',
 'quitting',
 'reader',
 'ready_to_run',
 'redirect_output',
 'remove_return_values_flag',
 'run',
 'send_caught_exception_stack',
 'send_caught_exception_stack_proceeded',
 'send_process_created_message',
 'send_process_will_be_substituted',
 'set_next_statement',
 'set_suspend',
 'set_trace_for_frame_and_parents',
 'set_tracing_for_untraced_contexts',
 'set_unit_tests_debugging_mode',
 'show_return_values',
 'signature_factory',
 'skip_on_exceptions_thrown_in_same_context',
 'skip_print_breakpoint_exception',
 'skip_suspend_on_breakpoint_exception',
 'start_auxiliary_daemon_threads',
 'stop_on_failed_tests',
 'stop_on_start',
 'stop_on_unhandled_exception',
 'stoptrace',
 'thread_analyser',
 'trace_dispatch',
 'use_frame_eval',
 'wait_for_commands',
 'writer']

