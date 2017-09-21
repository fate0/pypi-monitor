# -*- coding: utf-8 -*-

import os
import sys
import monkey

import pip.wheel
import pip.download
import pip.req.req_install
import pip.utils.setuptools_build


cur_dir = os.path.realpath(os.path.dirname(__file__))


# Shim to wrap setup.py invocation with setuptools
SETUPTOOLS_SHIM = (
    "import sys;sys.path.append(%r);" % cur_dir +
    "import setuptools, tokenize;__file__=%r;" +
    "import monkey; monkey.patch(%r);"
    "f=getattr(tokenize, 'open', open)(__file__);"
    "code=f.read().replace('\\r\\n', '\\n');"
    "f.close();"
    "exec(compile(code, __file__, 'exec'), globals(), locals());"
    "monkey.unpatch();" % sys.argv[-1]
)


pip.wheel.SETUPTOOLS_SHIM = SETUPTOOLS_SHIM
pip.download.SETUPTOOLS_SHIM =SETUPTOOLS_SHIM
pip.req.req_install.SETUPTOOLS_SHIM = SETUPTOOLS_SHIM
pip.utils.setuptools_build.SETUPTOOLS_SHIM = SETUPTOOLS_SHIM


if __name__ == '__main__':
    pip.main()
