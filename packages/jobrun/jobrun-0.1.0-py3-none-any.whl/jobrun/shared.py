from os import path
from pwd import getpwnam
from grp import getgrgid
from getpass import getuser 
from socket import gethostname
from abspathlib import AbsPath
from json5conf import JSONConfDict

config = JSONConfDict()
options = JSONConfDict()
parameterdict = {}
parameterpaths = []
interpolationdict = {}
script = JSONConfDict()
names = JSONConfDict()
nodes = JSONConfDict()
paths = JSONConfDict()
environ = JSONConfDict()
settings = JSONConfDict()
names.user = getuser()
names.host = gethostname()
paths.home = AbsPath(path.expanduser('~'))
paths.rundir = paths.home/'.jobrun'
paths.config = paths.rundir/'config'
