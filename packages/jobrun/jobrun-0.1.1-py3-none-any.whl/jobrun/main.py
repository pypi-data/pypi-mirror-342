import os
import re
import sys
import json
from socket import gethostname
from abspathlib import AbsPath, NotAbsolutePathError
from boolparse import BoolParser
from clinterface.printing import *
from json5conf import JSONConfDict

from .i18n import _
from .commandargs import parse_args
from .submission import configure_submission, submit_single_job
from .shared import names, nodes, paths, environ, config, options
from .utils import LogDict, GlobDict, ConfigTemplate, InterpolationTemplate, option, natural_sorted as sorted, catch_keyboard_interrupt, file_except_info

@catch_keyboard_interrupt
def submit_jobs(json_config):

    config.update(json.loads(json_config))
    names.command = os.path.basename(sys.argv[0])
    optiondict, argumentlist = parse_args(names, config)
    options.update(optiondict)
    configure_submission()

    if 'filter' in options.arguments:
        filtere = re.compile(options.arguments.filter)
    else:
        filtere = re.compile('.+')

    for inputfile in argumentlist:
        if options.common.job:
            workdir = AbsPath(options.common.indir)
            for key in config.inputfiles:
                if (workdir/inputfile%key).is_file():
                    inputname = inputfile
                    break
            else:
                print_failure(_('No hay archivos de entrada con nombre {inputname}'), inputname=inputfile, workdir=workdir)
                continue
        else:
            path = AbsPath(inputfile, relto=options.common.indir)
            try:
                path.assert_file()
            except Exception as e:
                file_except_info(e, path)
                continue
            for key in config.inputfiles:
                if path.name.endswith('.' + key):
                    inputname = path.name[:-len('.' + key)]
                    break
            else:
                print_failure(_('{file} no es un archivo de entrada de {package_name}'), file=path.name, package_name=config.packagename)
                continue
            workdir = path.parent
        filestatus = {}
        for key in config.filekeys:
            path = workdir/inputname%key
            filestatus[key] = path.is_file() #or key in options.restartfiles
        for conflict, message in config.conflicts.items():
            if BoolParser(conflict).evaluate(filestatus):
                print_failure(message, file=inputname)
                continue
        matched = filtere.fullmatch(inputname)
        if matched:
            filtergroups = {str(i): x for i, x in enumerate(matched.groups())}
            submit_single_job(workdir, inputname, filtergroups)

#if __name__ == '__main__':
#    run()
