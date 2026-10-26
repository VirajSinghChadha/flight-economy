# Builds ../index.html (the whole game in one file) from game.src.html + data.json
import os
here = os.path.dirname(os.path.abspath(__file__))
data = open(os.path.join(here, 'data.json'), encoding='utf8').read()
src = open(os.path.join(here, 'game.src.html'), encoding='utf8').read().replace('/*DATA*/null', data)
open(os.path.join(here, '..', 'index.html'), 'w', encoding='utf8').write(src)
print('built index.html', len(src), 'bytes')
