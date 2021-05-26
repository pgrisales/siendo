datos=[ {'x0':  105.47995780800001,  'x1':   291.4442955092628,  'y0':    621.537231385008,  'y1':     641.06314357464,},
      ]


control={'x0':  100,  'x1':  500,
'y0':    621.537231385008,  'y1':     641.06314357464,
        }

for dato in datos:
    print (dato)
    if dato['x0']>=control['x0'] and dato['x1']<=control['x1']:
        print('esta en x')
    if dato['y0']>=control['y0'] and dato['y1']<=control['y1']:
        print('esta en y')
    print ('-'*40)
