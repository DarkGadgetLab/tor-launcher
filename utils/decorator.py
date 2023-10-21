# -*- coding:utf-8 -*-
# builtins

# site-packages

# my-packages


__all__ = ['param_decorator']

def param_decorator(decorator):
    def param(*dec_args, **dec_kwargs):
        def executor(f):
            return decorator(f, *dec_args, **dec_kwargs)
        return executor
    return param
