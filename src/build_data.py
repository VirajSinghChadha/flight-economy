# Builds data.json (land polygons + all cities >=100k) from Natural Earth (world-atlas) and GeoNames cities15000.
import json, sys
src = sys.argv[1]
topo = json.load(open(src+'/land.json'))
sc, tr = topo['transform']['scale'], topo['transform']['translate']
arcs = []
for a in topo['arcs']:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy
        pts.append([round(x*sc[0]+tr[0], 2), round(y*sc[1]+tr[1], 2)])
    arcs.append(pts)
def ring(idx):
    out = []
    for i in idx:
        p = arcs[i] if i >= 0 else arcs[~i][::-1]
        out += p if not out else p[1:]
    return out
land = []
for g in topo['objects']['land']['geometries']:
    polys = g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]
    for poly in polys:
        land.append([ring(r) for r in poly])
cn = {}
for l in open(src+'/ci.txt', encoding='utf8'):
    if l.startswith('#'): continue
    f = l.rstrip('\n').split('\t')
    if len(f) > 4: cn[f[0]] = f[4]
cities = []
for l in open(src+'/cities15000.txt', encoding='utf8'):
    f = l.split('\t')
    pop = int(f[14])
    if pop >= 100000:
        cities.append([f[2], f[8], round(float(f[4]), 2), round(float(f[5]), 2), pop//1000])
# keep only cities that have an airport (OpenFlights) within 50 km; attach nearest IATA code
import csv, math
aps = []
for r in csv.reader(open(src+'/ap.dat', encoding='utf8')):
    if len(r) > 7 and len(r[4]) == 3 and r[4] != '\\N' and r[12] == 'airport':
        aps.append((r[4], float(r[6]), float(r[7])))
def hav(a, b, c, d):
    p = math.pi/180
    x = math.sin((c-a)*p/2)**2 + math.cos(a*p)*math.cos(c*p)*math.sin((d-b)*p/2)**2
    return 12742*math.asin(math.sqrt(x))
from collections import Counter
cnt = Counter()
for r in csv.reader(open(src+'/routes.dat', encoding='utf8')):
    if len(r) > 5: cnt[r[2]] += 1; cnt[r[4]] += 1
kept = []
for c in cities:
    best = None
    for code, la, lo in aps:
        if abs(la-c[2]) > 0.6 or abs(lo-c[3]) > 0.9/max(.2, math.cos(c[2]*math.pi/180)): continue
        d = hav(c[2], c[3], la, lo)
        if d <= 50 and cnt[code] > 0 and (best is None or cnt[code] > best[0]): best = (cnt[code], code)
    if best: kept.append(c + [best[1]])
print(len(cities), '->', len(kept), 'cities with an airport')
cities = kept
cities.sort(key=lambda c: -c[4])
ccs = sorted({c[1] for c in cities})
# port flag: city within 70 km of a coastline (110m land polygons, densified), plus a few island hubs the coarse coast misses
import collections
grid = collections.defaultdict(list)
for poly in land:
    for r in poly:
        for i in range(len(r)-1):
            x0, y0 = r[i]; x1, y1 = r[i+1]
            n = max(1, int(max(abs(x1-x0), abs(y1-y0))/0.25))
            for k in range(n+1):
                x = x0+(x1-x0)*k/n; y = y0+(y1-y0)*k/n
                grid[(int(math.floor(x)), int(math.floor(y)))].append((x, y))
FORCE = {'London','Hamburg','Antwerp','Rotterdam','Shanghai','Guangzhou','Houston','Philadelphia','Seville','Kolkata','Yangon','Bangkok','Ho Chi Minh City','Jakarta','Manila','Karachi','Lagos','Buenos Aires','Montevideo','Lisbon','Montreal','Saint Petersburg','New York City','Palma','Honolulu','Denpasar','Male','Cagliari','Valletta','Nassau','San Juan','Reykjavik','Havana','Piraeus','Heraklion','Funchal','Santa Cruz de Tenerife','Las Palmas de Gran Canaria','Hamilton','Bridgetown','Port of Spain','Victoria','Phuket','Cebu City','Colombo','Hong Kong','Singapore','Macau'}
for c in cities:
    cx, cy = int(math.floor(c[3])), int(math.floor(c[2]))
    port = 0
    for dx in (-2,-1,0,1,2):
        for dy in (-1,0,1):
            for (x, y) in grid.get((cx+dx, cy+dy), ()):
                if hav(c[2], c[3], y, x) < 70: port = 1; break
            if port: break
        if port: break
    c.append(1 if (port or c[0] in FORCE) else 0)
print(sum(c[6] for c in cities), 'port cities')
json.dump({'land': land, 'cities': cities, 'countries': {c: cn.get(c, c) for c in ccs}}, open('data.json', 'w'), separators=(',', ':'))
print(len(land), 'land polys,', len(cities), 'cities')
