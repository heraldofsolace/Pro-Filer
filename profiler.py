import argparse
from renderer import Renderer
from infogatherer import Infogatherer
from datetime import datetime
import os
import webbrowser

parser = argparse.ArgumentParser()
parser.add_argument('-s',action='store',type=int,help='Size',default=1000000,dest='s')
parser.add_argument('-p',action='store',type=str,help='Path',default=os.path.abspath(os.getcwd()),dest='p')
parser.add_argument('-f',action='store',type=str,help='Destination',default='out/output'+str(datetime.now())+'.html',dest='f')

args = parser.parse_args()
if not args.f.startswith('out/'):
    args.f = 'out/'+args.f
print('Scanning {}'.format(args.p))
print('This may take a while')
i = Infogatherer(args.p,options={'size':args.s})
r = Renderer(i.gather())
r.render(args.f)
webbrowser.open('file://'+os.path.abspath(args.f))

