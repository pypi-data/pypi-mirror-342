import inspect
import os

__all__ = ['nprint']

def nprint(*args, isp_details=False, sep=' '):
    if isp_details:
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)
        module_name = caller_info.filename
        line_number = caller_info.lineno
        class_name = caller_frame.f_locals.get('self', '').__class__.__name__
        print(f"{{{module_name}, {class_name}.class, Line {line_number}}}: ",*args, sep=sep)
    else:
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)
        module_name = os.path.basename(caller_info.filename)
        line_number = caller_info.lineno
        print(f"{{{module_name}, Line {line_number}}}: ", *args, sep=sep)
