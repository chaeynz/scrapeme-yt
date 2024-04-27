# pylint: disable=missing-docstring
import sys

INNERTUBE_CLIENT_NAME = ""

def trace_calls(frame, event, arg):
    global INNERTUBE_CLIENT_NAME # pylint: disable=global-statement
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'player':  # Target function name
        local_vars = frame.f_locals
        print(f"Inside {func_name}: ", local_vars)  # Inspect local variables
        # If you need to do something with a specific variable:
        if 'self' in local_vars:
            INNERTUBE_CLIENT_NAME = f"{local_vars['self'].context['client']['clientName']}"


def setup_tracer():
    sys.settrace(trace_calls)
