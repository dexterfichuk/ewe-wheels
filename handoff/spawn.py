import csv, math, collections, sys
f = sys.argv[1]
lat0, lon0 = 50.751, -126.497  # Salmon Coast Field Station, Echo Bay
def km(a,b,c,d):
    return 6371*2*math.asin(math.sqrt(math.sin(math.radians(c-a)/2)**2+math.cos(math.radians(a))*math.cos(math.radians(c))*math.sin(math.radians(d-b)/2)**2))
yr = collections.defaultdict(lambda:[0,0.0,0.0]); sections=collections.Counter(); locs=collections.Counter()
for r in csv.DictReader(open(f)):
    try: la, lo = float(r['Latitude']), float(r['Longitude'])
    except: continue
    if km(lat0,lon0,la,lo) > 15: continue
    def v(k):
        try: return float(r[k])
        except: return 0.0
    y = int(r['Year']); idx = v('Surface')+v('Macrocystis')+v('Understory')
    yr[y][0]+=1; yr[y][1]+=idx; yr[y][2]+=v('Length')
    sections[r['Section']]+=1; locs[r['LocationName']]+=1
print('sections', sections.most_common(10)); print('locs', locs.most_common(15))
with open('broughton_spawn_index.csv','w') as o:
    o.write('year,n_spawns,spawn_index_t,length_m\n')
    for y in range(1951,2026):
        n,i,l = yr.get(y,[0,0,0]); o.write(f'{y},{n},{i:.1f},{l:.0f}\n')
