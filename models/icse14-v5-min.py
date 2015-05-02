from __future__ import division
import sys,collections,random
sys.dont_write_bytecode = True

def shuffle(lst):
  random.shuffle(lst)
  return lst

class Thing():
  id = -1
  def __init__(i,**fields) : 
    i.override(fields)
    i._id = Thing.id = Thing.id + 1
    i.finalize()
  def finalize(i): pass
  def override(i,d): i.__dict__.update(d); return i
  def plus(i,**d): i.override(d)
  def __repr__(i):
    d = i.__dict__
    name = i.__class__.__name__
    return name+'{'+' '.join([':%s %s' % (k,pretty(d[k])) 
                     for k in i.show()])+ '}'
  def show(i):
    return [k for k in sorted(i.__dict__.keys()) 
            if not "_" in k]

def tunings( _ = None):
  return dict( 
    Flex= [5.07, 4.05, 3.04, 2.03, 1.01,    _],
    Pmat= [7.80, 6.24, 4.68, 3.12, 1.56,    _],
    Prec= [6.20, 4.96, 3.72, 2.48, 1.24,    _],
    Resl= [7.07, 5.65, 4.24, 2.83, 1.41,    _],
    Team= [5.48, 4.38, 3.29, 2.19, 1.01,    _], 
    acap= [1.42, 1.19, 1.00, 0.85, 0.71,    _], 
    aexp= [1.22, 1.10, 1.00, 0.88, 0.81,    _], 
    cplx= [0.73, 0.87, 1.00, 1.17, 1.34, 1.74], 
    data= [   _, 0.90, 1.00, 1.14, 1.28,    _], 
    docu= [0.81, 0.91, 1.00, 1.11, 1.23,    _],
    ltex= [1.20, 1.09, 1.00, 0.91, 0.84,    _], 
    pcap= [1.34, 1.15, 1.00, 0.88, 0.76,    _], 
    pcon= [1.29, 1.12, 1.00, 0.90, 0.81,    _], 
    plex= [1.19, 1.09, 1.00, 0.91, 0.85,    _], 
    pvol= [   _, 0.87, 1.00, 1.15, 1.30,    _], 
    rely= [0.82, 0.92, 1.00, 1.10, 1.26,    _], 
    ruse= [   _, 0.95, 1.00, 1.07, 1.15, 1.24], 
    sced= [1.43, 1.14, 1.00, 1.00, 1.00,    _], 
    site= [1.22, 1.09, 1.00, 0.93, 0.86, 0.80], 
    stor= [   _,    _, 1.00, 1.05, 1.17, 1.46], 
    time= [   _,    _, 1.00, 1.11, 1.29, 1.63], 
    tool= [1.17, 1.09, 1.00, 0.90, 0.78,    _])



Features=dict(Sf=[ 'Prec','Flex','Resl','Team','Pmat'],
              Prod=['rely','data','cplx','ruse','docu'],
              Platform=['time','stor','pvol'],
              Person=['acap','pcap','pcon','aexp','plex','ltex'],
              Project=['tool','site','sced'])

def options():
  return Thing(levels=10,samples=20,shrink=0.66,round=2,epsilon=0.00,
               guesses=1000)


Features=dict(Sf=[ 'Prec','Flex','Resl','Team','Pmat'],
              Prod=['rely','data','cplx','ruse','docu'],
              Platform=['time','stor','pvol'],
              Person=['acap','pcap','pcon','aexp','plex','ltex'],
              Project=['tool','site','sced'])

def has(x,lst):
 try:
   out=lst.index(x)
   return out
 except ValueError:
    return None



def nasa93(opt=options(),tunings=tunings()):
  vl=1;l=2;n=3;h=4;vh=5;xh=6
  return Thing(
    sfem=21,
    kloc=22,
    effort=23,
    names= [ 
     # 0..8
     'Prec', 'Flex', 'Resl', 'Team', 'Pmat', 'rely', 'data', 'cplx', 'ruse',
     # 9 .. 17
     'docu', 'time', 'stor', 'pvol', 'acap', 'pcap', 'pcon', 'aexp', 'plex',  
     # 18 .. 25
     'ltex', 'tool', 'site', 'sced', 'kloc', 'effort', '?defects', '?months'],
    projects=[
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,25.9,117.6,808,15.3],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,24.6,117.6,767,15.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,7.7,31.2,240,10.1],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,8.2,36,256,10.4],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,9.7,25.2,302,11.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,2.2,8.4,69,6.6],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,3.5,10.8,109,7.8],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,352.8,2077,21.0],
	[h,h,h,vh,h,h,l,h,n,n,xh,xh,l,h,h,n,h,n,h,h,n,n,7.5,72,226,13.6],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,20,72,566,14.4],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,6,24,188,9.9],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,100,360,2832,25.2],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,vh,n,l,n,n,n,11.3,36,456,12.8],
	[h,h,h,vh,n,n,l,h,n,n,n,n,h,h,h,n,h,l,vl,n,n,n,100,215,5434,30.1],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,20,48,626,15.1],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,n,n,vl,n,n,n,100,360,4342,28.0],
	[h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,vh,n,vh,n,h,n,n,n,150,324,4868,32.5],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,h,n,h,n,n,n,31.5,60,986,17.6],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,15,48,470,13.6],
	[h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,n,n,h,n,h,n,n,n,32.5,60,1276,20.8],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,19.7,60,614,13.9],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,300,2077,21.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,29.5,120,920,16.0],
	[h,h,h,vh,n,h,n,n,n,n,h,n,n,n,h,n,h,n,n,n,n,n,15,90,575,15.2],
	[h,h,h,vh,n,h,n,h,n,n,n,n,n,n,h,n,h,n,n,n,n,n,38,210,1553,21.3],
	[h,h,h,vh,n,n,n,n,n,n,n,n,n,n,h,n,h,n,n,n,n,n,10,48,427,12.4],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,15.4,70,765,14.5],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,48.5,239,2409,21.4],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,16.3,82,810,14.8],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,12.8,62,636,13.6],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,32.6,170,1619,18.7],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,35.5,192,1763,19.3],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,5.5,18,172,9.1],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,10.4,50,324,11.2],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,14,60,437,12.4],
	[h,h,h,vh,n,h,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,6.5,42,290,12.0],
	[h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,13,60,683,14.8],
	[h,h,h,vh,h,n,n,h,n,n,n,n,n,n,h,n,n,n,h,h,n,n,90,444,3343,26.7],
	[h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,8,42,420,12.5],
	[h,h,h,vh,n,n,n,h,n,n,h,n,n,n,n,n,n,n,n,n,n,n,16,114,887,16.4],
	[h,h,h,vh,h,n,h,h,n,n,vh,h,l,h,h,n,n,l,h,n,n,l,177.9,1248,7998,31.5],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,h,n,n,n,n,n,n,n,302,2400,8543,38.4],
	[h,h,h,vh,h,n,h,l,n,n,n,n,h,h,n,n,h,n,n,h,n,n,282.1,1368,9820,37.3],
	[h,h,h,vh,h,h,h,l,n,n,n,n,n,h,n,n,h,n,n,n,n,n,284.7,973,8518,38.1],
	[h,h,h,vh,n,h,h,n,n,n,n,n,l,n,h,n,h,n,h,n,n,n,79,400,2327,26.9],
	[h,h,h,vh,l,l,n,n,n,n,n,n,l,h,vh,n,h,n,h,n,n,n,423,2400,18447,41.9],
	[h,h,h,vh,h,n,n,n,n,n,n,n,l,h,vh,n,vh,l,h,n,n,n,190,420,5092,30.3],
	[h,h,h,vh,h,n,n,h,n,n,n,h,n,h,n,n,h,n,h,n,n,n,47.5,252,2007,22.3],
	[h,h,h,vh,l,vh,n,xh,n,n,h,h,l,n,n,n,h,n,n,h,n,n,21,107,1058,21.3],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,78,571.4,4815,30.5],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,11.4,98.8,704,15.5],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,19.3,155,1191,18.6],
	[h,h,h,vh,l,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,101,750,4840,32.4],
	[h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,219,2120,11761,42.8],
	[h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,50,370,2685,25.4],
	[h,h,h,vh,h,vh,h,h,n,n,vh,vh,n,vh,vh,n,vh,n,h,h,n,l,227,1181,6293,33.8],
	[h,h,h,vh,h,n,h,vh,n,n,n,n,l,h,vh,n,n,l,n,n,n,l,70,278,2950,20.2],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,0.9,8.4,28,4.9],
	[h,h,h,vh,l,vh,l,xh,n,n,xh,vh,l,h,h,n,vh,vl,h,n,n,n,980,4560,50961,96.4],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,vh,vh,n,n,h,h,n,n,n,350,720,8547,35.7],
	[h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,70,458,2404,27.5],
	[h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,271,2460,9308,43.4],
	[h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,90,162,2743,25.0],
	[h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,40,150,1219,18.9],
	[h,h,h,vh,n,h,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,137,636,4210,32.2],
	[h,h,h,vh,n,h,n,h,n,n,h,n,h,h,h,n,h,n,h,n,n,n,150,882,5848,36.2],
	[h,h,h,vh,n,vh,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,339,444,8477,45.9],
	[h,h,h,vh,n,l,h,l,n,n,n,n,h,h,h,n,h,n,h,n,n,n,240,192,10313,37.1],
	[h,h,h,vh,l,h,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,144,576,6129,28.8],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,151,432,6136,26.2],
	[h,h,h,vh,l,n,l,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,34,72,1555,16.2],
	[h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,98,300,4907,24.4],
	[h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,85,300,4256,23.2],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,20,240,813,12.8],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,111,600,4511,23.5],
	[h,h,h,vh,l,h,vh,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,162,756,7553,32.4],
	[h,h,h,vh,l,h,h,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,352,1200,17597,42.9],
	[h,h,h,vh,l,h,n,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,165,97,7867,31.5],
	[h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,60,409,2004,24.9],
	[h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,100,703,3340,29.6],
	[h,h,h,vh,n,h,vh,vh,n,n,xh,xh,h,n,n,n,n,l,l,n,n,n,32,1350,2984,33.6],
	[h,h,h,vh,h,h,h,h,n,n,vh,xh,h,h,h,n,h,h,h,n,n,n,53,480,2227,28.8],
	[h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,41,599,1594,23.0],
	[h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,24,430,933,19.2],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,165,4178.2,6266,47.3],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,65,1772.5,2468,34.5],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,70,1645.9,2658,35.4],
	[h,h,h,vh,h,vh,h,xh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,50,1924.5,2102,34.2],
	[h,h,h,vh,l,vh,l,vh,n,n,vh,xh,l,h,n,n,l,vl,l,h,n,n,7.25,648,406,15.6],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,233,8211,8848,53.1],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,16.3,480,1253,21.5],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  6.2, 12,477,15.4],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  3.0, 38,231,12.0],
	])


def coc81(opt=options(),tunings=tunings()):
  vl=1;l=2;n=3;h=4;vh=5;xh=6
  return Thing(
    sfem=21,
    kloc=22,
    effort=23,
    names= [
     'Prec', 'Flex', 'Resl', 'Team', 'Pmat', 'rely', 'data', 'cplx', 'ruse',
     'docu', 'time', 'stor', 'pvol', 'acap', 'pcap', 'pcon', 'aexp', 'plex',  
     'ltex', 'tool', 'site', 'sced', 'kloc', 'effort', '?defects', '?months'],
    projects=[
      [h,h,h,vh,vl,l,vh,vl,n,n,n,h,h,l,l,n,l,l,n,vl,h,n,113,2040,13027,38.4],
      [h,h,h,vh,vl,l,vh,l,n,n,n,h,n,n,n,n,h,h,h,vl,h,n,293,1600,25229,48.6],
      [h,h,h,vh,n,n,vh,l,n,n,n,n,l,h,h,n,vh,h,h,l,h,n,132,243,3694,28.7],
      [h,h,h,vh,vl,vl,vh,vl,n,n,n,n,l,l,vl,n,h,n,h,vl,h,n,60,240,5688,28.0],
      [h,h,h,vh,vl,l,l,n,n,n,n,n,l,n,h,n,n,h,h,vl,h,n,16,33,970,14.3],
      [h,h,h,vh,vl,vl,n,l,n,n,n,vh,n,vl,vl,n,n,h,h,vl,h,n,4,43,553,11.6],
      [h,h,h,vh,n,vl,n,n,n,n,n,n,l,n,n,n,n,h,h,l,h,n,6.9,8,350,10.3],
      [h,h,h,vh,vl,h,l,vh,n,n,xh,xh,vh,vh,n,n,h,vl,vl,vl,h,l,22,1075,3511,24.5],
      [h,h,h,vh,n,h,l,vh,n,n,vh,vh,h,h,h,n,n,l,l,vl,h,n,30,423,1989,24.1],
      [h,h,h,vh,l,vh,l,vh,n,n,h,xh,n,h,h,n,vh,h,n,vl,h,n,29,321,1496,23.2],
      [h,h,h,vh,l,vh,l,vh,n,n,h,xh,n,h,h,n,vh,h,n,vl,h,n,32,218,1651,24.0],
      [h,h,h,vh,n,h,l,vh,n,n,h,h,n,h,h,n,vh,n,h,vl,h,l,37,201,1783,19.1],
      [h,h,h,vh,n,h,l,vh,n,n,h,h,h,vh,vh,n,n,l,n,vl,h,n,25,79,1138,18.4],
      [h,h,h,vh,vl,h,l,xh,n,n,vh,xh,h,h,vh,n,n,l,l,vl,h,vl,3,60,387,9.4],
      [h,h,h,vh,n,vh,l,vh,n,n,vh,h,h,h,h,n,l,vl,vl,vl,h,vl,3.9,61,276,9.5],
      [h,h,h,vh,l,vh,n,vh,n,n,vh,xh,n,h,h,n,n,n,n,vl,h,n,6.1,40,390,14.9],
      [h,h,h,vh,l,vh,n,vh,n,n,vh,xh,n,h,h,n,vh,n,n,vl,h,n,3.6,9,230,12.3],
      [h,h,h,vh,vl,h,vh,h,n,n,vh,vh,n,h,n,n,n,n,n,vl,h,l,320,11400,34588,52.4],
      [h,h,h,vh,n,h,h,n,n,n,h,vh,l,vh,n,n,h,n,n,l,h,n,1150,6600,41248,67.0],
      [h,h,h,vh,vl,vh,h,vh,n,n,h,vh,h,vh,n,n,vh,l,l,vl,h,l,299,6400,30955,53.4],
      [h,h,h,vh,n,n,vh,h,n,n,n,n,l,h,n,n,n,n,n,l,h,n,252,2455,11664,40.8],
      [h,h,h,vh,n,h,n,n,n,n,n,h,n,h,h,n,vh,h,n,vl,h,vl,118,724,5172,21.7],
      [h,h,h,vh,l,h,n,n,n,n,n,h,n,h,h,n,vh,h,n,vl,h,vl,77,539,4362,19.5],
      [h,h,h,vh,n,l,n,l,n,n,n,h,n,n,n,n,vl,l,h,n,h,n,90,453,4407,27.1],
      [h,h,h,vh,n,h,vh,vh,n,n,n,h,n,h,h,n,n,l,n,l,h,l,38,523,2269,20.2],
      [h,h,h,vh,n,n,n,l,n,n,n,h,h,h,h,n,n,l,n,vl,h,l,48,387,2419,18.5],
      [h,h,h,vh,n,h,l,h,n,n,n,vh,n,n,n,n,n,n,n,vl,h,l,9.4,88,517,12.1],
      [h,h,h,vh,vl,h,h,vh,n,n,h,vh,h,h,h,n,n,l,l,vl,h,n,13,98,1473,19.6],
      [h,h,h,vh,n,l,n,n,n,n,n,n,n,n,h,n,vl,n,n,l,h,vl,2.14,7.3,138,5.3],
      [h,h,h,vh,n,l,n,n,n,n,n,n,n,n,h,n,vl,n,n,l,h,vl,1.98,5.9,128,5.2],
      [h,h,h,vh,l,vh,h,n,n,n,n,xh,h,h,h,n,vh,l,l,vl,h,n,62,1063,3682,32.8],
      [h,h,h,vh,vl,l,h,l,n,n,n,n,n,vh,n,n,vh,n,n,vl,h,n,390,702,30484,45.8],
      [h,h,h,vh,n,vh,h,vh,n,n,n,xh,h,h,h,n,vh,h,n,l,h,n,42,605,1803,27.1],
      [h,h,h,vh,n,h,h,n,n,n,n,n,n,n,n,n,n,n,n,vl,h,vl,23,230,1271,14.2],
      [h,h,h,vh,vl,vl,l,vh,n,n,n,vh,h,n,n,n,h,l,n,vl,h,n,13,82,2250,17.2],
      [h,h,h,vh,l,l,n,n,n,n,n,n,l,l,l,n,n,h,h,l,h,n,15,55,1004,15.8],
      [h,h,h,vh,l,l,l,vl,n,n,n,h,n,h,h,n,vh,n,n,vl,h,n,60,47,2883,20.3],
      [h,h,h,vh,n,n,n,h,n,n,n,n,l,vh,n,n,h,h,h,l,h,n,15,12,504,13.5],
      [h,h,h,vh,n,n,n,h,n,n,n,n,l,vh,vh,n,vh,n,h,vl,h,n,6.2,8,197,9.6],
      [h,h,h,vh,vl,n,l,vh,n,n,n,n,n,h,l,n,vh,n,n,vl,h,n,n,8,294,9.5],
      [h,h,h,vh,n,l,l,n,n,n,n,n,l,n,vh,n,vh,h,h,l,h,n,5.3,6,173,8.7],
      [h,h,h,vh,l,l,n,n,n,n,n,h,l,h,n,n,n,h,h,vl,h,n,45.5,45,2645,21.0],
      [h,h,h,vh,l,n,n,n,n,n,n,vh,l,h,n,n,n,h,h,vl,h,n,28.6,83,1416,18.9],
      [h,h,h,vh,vl,l,n,n,n,n,n,vh,l,n,n,n,n,h,h,vl,h,n,30.6,87,2444,20.5],
      [h,h,h,vh,l,l,n,n,n,n,n,h,l,n,n,n,n,h,h,vl,h,n,35,106,2198,20.1],
      [h,h,h,vh,l,l,n,n,n,n,n,h,l,n,h,n,n,h,h,vl,h,n,73,126,4188,25.1],
      [h,h,h,vh,vl,vl,l,vh,n,n,n,n,l,vh,vh,n,vh,l,l,vl,h,n,23,36,2161,15.6],
      [h,h,h,vh,vl,l,l,l,n,n,n,n,l,l,l,n,h,h,h,vl,h,n,464,1272,32002,53.4],
      [h,h,h,vh,n,n,n,l,n,n,n,n,n,vh,vh,n,n,l,n,l,h,n,91,156,2874,22.6],
      [h,h,h,vh,l,h,n,n,n,n,vh,vh,n,h,h,n,n,l,n,vl,h,n,24,176,1541,20.3],
      [h,h,h,vh,vl,l,n,n,n,n,n,n,n,l,vl,n,n,n,h,vl,h,n,10,122,1225,16.2],
      [h,h,h,vh,vl,l,l,l,n,n,n,h,h,n,n,n,n,l,l,vl,h,n,8.2,41,855,13.1],
      [h,h,h,vh,l,l,l,h,n,n,h,vh,vh,vh,vh,n,n,l,l,vl,h,l,5.3,14,533,9.3],
      [h,h,h,vh,n,n,l,n,n,n,n,h,h,n,n,n,vh,n,h,vl,h,n,4.4,20,216,10.6],
      [h,h,h,vh,vl,l,l,vl,n,n,n,n,l,h,l,n,vh,h,h,vl,h,n,6.3,18,309,9.6],
      [h,h,h,vh,vl,h,l,vh,n,n,vh,vh,n,h,n,n,h,l,l,vl,h,l,27,958,3203,21.1],
      [h,h,h,vh,vl,n,l,h,n,n,h,vh,vh,n,n,n,n,l,l,vl,h,vl,17,237,2622,16.0],
      [h,h,h,vh,n,vh,l,vh,n,n,xh,vh,n,vh,vh,n,vh,h,h,vl,h,n,25,130,813,20.9],
      [h,h,h,vh,n,n,l,h,n,n,n,h,n,n,n,n,n,n,n,vl,h,n,23,70,1294,18.2],
      [h,h,h,vh,vl,h,l,vh,n,n,h,h,n,h,h,n,l,l,l,vl,h,l,6.7,57,650,11.3],
      [h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,n,h,n,vl,h,n,28,50,997,16.4],
      [h,h,h,vh,n,l,l,vh,n,n,h,vh,h,n,vh,n,vh,vl,vl,vl,h,n,9.1,38,918,15.3],
      [h,h,h,vh,n,n,l,h,n,n,n,n,n,vh,h,n,vh,n,n,vl,h,n,10,15,418,11.6],
      ])



def sdiv(lst, tiny=3,cohen=0.3,
         num1=lambda x:x[0], num2=lambda x:x[1]):
  "Divide lst of (num1,num2) using variance of num2."
  #----------------------------------------------
  class Counts(): # Add/delete counts of numbers.
    def __init__(i,inits=[]):
      i.zero()
      for number in inits: i + number 
    def zero(i): i.n = i.mu = i.m2 = 0.0
    def sd(i)  : 
      if i.n < 2: return i.mu
      else:       
        return (max(0,i.m2)*1.0/(i.n - 1))**0.5
    def __add__(i,x):
      i.n  += 1
      delta = x - i.mu
      i.mu += delta/(1.0*i.n)
      i.m2 += delta*(x - i.mu)
    def __sub__(i,x):
      if i.n < 2: return i.zero()
      i.n  -= 1
      delta = x - i.mu
      i.mu -= delta/(1.0*i.n)
      i.m2 -= delta*(x - i.mu)    

  #----------------------------------------------
  def divide(this,small): #Find best divide of 'this'
    lhs,rhs = Counts(), Counts(num2(x) for x in this)
    n0, least, cut = 1.0*rhs.n, rhs.sd(), None
    for j,x  in enumerate(this): 
      if lhs.n > tiny and rhs.n > tiny: 
        maybe= lhs.n/n0*lhs.sd()+ rhs.n/n0*rhs.sd()
        if maybe < least :  
          if abs(lhs.mu - rhs.mu) >= small:
            cut,least = j,maybe
      rhs - num2(x)
      lhs + num2(x)    
    return cut,least
  #----------------------------------------------
  def recurse(this, small,cuts):
    cut,sd = divide(this,small)
    if cut: 
      recurse(this[:cut], small, cuts)
      recurse(this[cut:], small, cuts)
    else:   
      cuts += [(sd * len(this)/len(lst),this)]
    return cuts
  #---| main |-----------------------------------
  small = Counts(num2(x) for x in lst).sd()*cohen
  if lst: 
    return recurse(sorted(lst,key=num1),small,[])

def fss(d=coc81(),want=0.25):
  rank=[]
  for i in range(d.sfem):
    xs=sdiv(d.projects,
         num1=lambda x:x[i],
         num2=lambda x:x[d.effort])
    xpect = sum(map(lambda x: x[0],xs))
    rank += [(xpect,i)]
  rank = sorted(rank)
  keep = int(len(rank)*want)
  doomed= map(lambda x:x[1], rank[keep:])
  for project in d.projects:
    for col in doomed:
      project[col] = 3
  return d

def less(d=coc81(),n=2):
  skipped = 0
  names0 = d.names
  toUse,doomed = [],[]
  for v in Features.values():
    toUse += v[:n]
  for n,name in enumerate(names0):
    if n >= d.sfem:
      break
    if not has(name,toUse):
      doomed += [n]
  for project in d.projects:
    for col in doomed:
      project[col] = 3
  return d

def meanr(lst):
  total=n=0.00001
  for x in lst:
    if not x == None:
      total += x
      n += 1
  return total/n

def tothree(lst):
  below=lst[:2]
  above=lst[3:]
  m1 = meanr(below)
  m2=  meanr(above)
  below = [m1 for _ in below]
  above = [m2 for _ in above]
  return below + [lst[2]] + above

def rr3(lst):
  #return lst 
  r = 1
  if lst[0]> 2 : r = 0
  def rr1(n): return round(x,r) if x else None
  tmp= tothree([rr1(x) for x in lst])
  return tmp

def rr5(lst):
  if lst[0] > 2:
    return [6,5,4,3,2,1]
  if lst[0] < 0:
    return [0.8, 0.9, 1, 1.1, 1.2, 1.3]
  return   [1.2,1.1,1,0.9,0.8,0.7]

def rrs5(d):
  for k in d: d[k] = rr5(d[k])
  return d

def rrs3(d):
  for k in d: d[k] = rr3(d[k])
  return d


def detune(m,tun=tunings()):
  def best(at,one,lst):
    least,x = 100000,None
    for n,item in enumerate(lst):
      if item:
        tmp = abs(one - item)
        if tmp < least:
          least = tmp
          x = n
    return x
  def detuned(project):
    for n,(name,val) in  enumerate(zip(m.names,project)):
      if n <= m.sfem:
        project[n] = best(n,val,tun[name]) + 1
    return project
  m.projects = [detuned(project) for 
                project in m.projects]
  for p in m.projects: print p
  return m


#########################################
# begin code

## imports
import random,math,sys
r    = random.random
any  = random.choice
seed = random.seed
exp  = lambda n: math.e**n
ln   = lambda n: math.log(n,math.e)
g    = lambda n: round(n,2)
def say(x):
  sys.stdout.write(str(x))
  sys.stdout.flush() 

def nl(): print ""
## classes
class Score(Thing):
  def finalize(i) : 
    i.all = []
    i.residuals=[]
    i.raw=[]
    i.use=False
  def seen(i,got,want): 
    i.residuals += [abs(got - want)]
    i.raw += [got - want]
    tmp = i.mre(got,want)
    i.all += [tmp]
    return tmp
  def mar(i):
    return median(sorted(i.residuals))
    #return sum(i.residuals) / len(i.residuals)
  def sanity(i,baseline):  
    return i.mar()*1.0/baseline
  def mre(i,got,want): 
    return abs(got- want)*1.0/(0.001+want)
  def mmre(i): 
    return sum(i.all)*1.0/len(i.all)
  def medre(i): 
    return median(sorted(i.all))
  def pred(i,n=30):
    total = 0.0
    for val in i.all:
      if val <= n*0.01: total += 1
    return total*1.0/len(i.all) 

## low-level utils
def pretty(s):
  if isinstance(s,float):
    return '%.3f' % s
  else: return '%s' % s



def stats(l,ordered=False):
  if not ordered: l= sorted(l)
  p25= l[len(l)/4]
  p50= l[len(l)/2]  
  p75= l[len(l)*3/4]
  p100= l[-1]
  print p50, p75-p25, p100

## mode prep
def valued(d,opt,t=tunings()):
  for old in d.projects:
    for i,name in enumerate(d.names):
      if i <= d.sfem:
        tmp = old[i]
        if not isinstance(tmp,float):
          tmp  = old[i] - 1
          old[i] = round(t[name][tmp],opt.round)
  return d

####################################

def median(lst,ordered=False):
  if not ordered: lst= sorted(lst)
  n = len(lst)
  if n==0: return 0
  if n==1: return lst[0]
  if n==2: return (lst[0] + lst[1])*0.5
  if n % 2: return lst[n//2]
  n = n//2
  return (lst[n] + lst[n+1]) * 0.5

class Count:
  def __init__(i,name="counter"):
    i.name=name
    i.lo =    10**32
    i.hi= -1*10**32
    i._all = []
    i._also = None
  def keep(i,n):
    i._also= None
    if n > i.hi: i.hi = n
    if n < i.lo: i.lo = n
    i._all += [n]
  def centroid(i):return i.also().median
  def all(i): return i.also().all
  def also(i):
    if not i._also:
      i._all = sorted(i._all)
      if not i._all: 
        i._also = Thing(all=i._all,
                        median=0)
      else:
        i._also = Thing(all=i._all,
                      median=median(i._all))
    return i._also
  def norm(i,n):
    #return n
    return (n - i.lo)*1.0 / (i.hi - i.lo + 0.0001)

def clone(old,data=[]):
  return Model(map(lambda x: x.name,old.headers),
              data)

class Model:
  def __init__(i,names,data=[],indep=0):
    i.indep = indep
    i.headers = [Count(name) for name in names]
    i._also = None
    i.rows = []
    for row in data: i.keep(row)
  def centroid(i): return i.also().centroid
  def xy(i)      : return i.also().xy
  def also(i):
    if not i._also:
      xs, ys  = 0,0
      for row in i.rows:
        xs += row.x
        ys += row.y
      n = len(i.rows)+0.0001
      i._also=  Thing(
        centroid= map(lambda x: x.centroid(), 
                      i.headers),
        xy      = (xs/n, ys/n))
    return i._also
  def keep(i,row):
    i._also = None
    if isinstance(row,Row):
      content=row.cells
    else:
      content=row
      row = Row(cells=row)
    for cell,header in zip(content,i.headers):
      header.keep(cell)
    i.rows += [row]
   

class Row(Thing):
  def finalize(i):
    i.x = i.y = 0
  def xy(i,x,y):
    if not i.x:
      i.x, i.y = x,y 
  

def lo(m,x)     : return m.headers[x].lo
def hi(m,x)     : return m.headers[x].hi
def norm(m,x,n) : return m.headers[x].norm(n)

def cosineRule(z,m,c,west,east,slots):
  a = dist(m,z,west,slots)
  b = dist(m,z,east,slots)
  x= (a*a + c*c - b*b)/(2*c+0.00001) # cosine rule
  y= max(0,a**2 - x**2)**0.5
  return x,y

def fastmap(m,data,slots):
  "Divide data into two using distance to two distant items."
  one  = any(data)             # 1) pick anything
  west = furthest(m,one,data,slots)  # 2) west is as far as you can go from anything
  east = furthest(m,west,data,slots) # 3) east is as far as you can go from west
  c    = dist(m,west,east,slots)
  # now find everyone's distance
  lst = []
  for one in data:
    x,y= cosineRule(one,m,c,west,east,slots)
    one.xy(x,y)
    lst  += [(x, one)]
  lst = sorted(lst)
  wests,easts = [], []
  cut  = len(lst) // 2
  cutx = lst[cut][0]
  for x,one in  lst:
    what  = wests if x <= cutx else easts
    what += [one]
  return wests,west, easts,east,cutx,c

def dist(m,i,j,slots):
  "Euclidean distance 0 <= d <= 1 between decisions"
  d1,d2  = slots.what(i), slots.what(j)
  n      = len(d1)
  deltas = 0
  for d in range(n):
    n1 = norm(m, d, d1[d])
    n2 = norm(m, d, d2[d])
    inc = (n1-n2)**2
    deltas += inc
  return deltas**0.5 / n**0.5

def furthest(m,i,all,slots,
             init = 0,
             better = lambda x,y: x>y):
  "find which of all is furthest from 'i'"
  out,d= i,init
  for j in all:
    if not i == j:
      tmp = dist(m,i,j,slots)
      if better(tmp,d): out,d = j,tmp
  return out

def myCentroid(row,t):
  x1,y1=row.x,row.y
  out,d=None,10**32
  for leaf in leaves(t):
    x2,y2=leaf.m.xy()
    tmp = ((x2-x1)**2 + (y2-y1)**2)**0.5
    if tmp < d:
      out,d=leaf,tmp
  return out

def centroid2(row,t):
  x1,y1=row.x,row.y
  out=[]
  for leaf in leaves(t):
    x2,y2 = leaf.m.xy()
    tmp = ((x2-x1)**2 + (y2-y1)**2)**0.5
    out += [(tmp,leaf)]
  out = sorted(out)
  if len(out)==0:
    return [(None,None),(None,None)]
  if len(out) ==1:
    return out[0],out[0]
  else:
    return out[0],out[1]

    

def where0(**other):
  return Thing(minSize  = 10,    # min leaf size
               depthMin= 2,      # no pruning till this depth
               depthMax= 10,     # max tree depth
               b4      = '|.. ', # indent string
               verbose = False,  # show trace info?
               what    = lambda x: x.cells
   ).override(other)


def where(m,data,slots=None):
  slots = slots or where0()
  return where1(m,data,slots,0,10**32)

def where1(m, data, slots, lvl, sd0,parent=None):
  here = Thing(m=clone(m,data),
               up=parent,
               _west=None,_east=None,leafp=False)
  def tooDeep(): return lvl > slots.depthMax
  def tooFew() : return len(data) < slots.minSize
  def show(suffix): 
    if slots.verbose: 
      print slots.b4*lvl + str(len(data)) + suffix
  if tooDeep() or tooFew():
    show(".")
    here.leafp=True
  else:
    show("1")    
    wests,west, easts,east,cut,c = fastmap(m,data,slots)
    here.plus(c=c, cut=cut, west=west, east=east)
    sd1=Num("west",[slots.klass(w) for w in wests]).spread()
    sd2=Num("east",[slots.klass(e) for e in easts]).spread()
    goWest = goEast = True
    if lvl > 0:
      goWest = sd1 < sd0
      goEast = sd2 < sd0
    if  goWest:
      here._west = where1(m, wests, slots, lvl+1, sd1,here)
    if  goEast:
      here._east = where1(m, easts, slots, lvl+1, sd2,here)
  return here

def leaf(t,row,slots,lvl=1):
  if t.leafp: 
    return t
  else:
    x,_ = cosineRule(row, t.m, t.c,t.west,t.east,slots)
    return leaf(t._west if x <= t.cut else t._east,
                row,slots,lvl+1)

def preOrder(t):
  if t:
    yield t
    for kid in [t._west,t._east]:
      for out in preOrder(kid):
        yield out
      
def leaves(t):
  for t1 in preOrder(t):
    if t1.leafp:
      yield t1
          
def tprint(t,lvl=0):
  if t:
    print '|.. '*lvl + str(len(t.m.rows)), '#'+str(t._id)
    tprint(t._west,lvl+1)
    tprint(t._east,lvl+1)

import sys,math,random
sys.dont_write_bytecode = True

def go(f):
  "A decorator that runs code at load time."
  print "\n# ---|", f.__name__,"|-----------------"
  if f.__doc__: print "#", f.__doc__
  f()

# random stuff
seed = random.seed
any  = random.choice

# pretty-prints for list
def gs(lst) : return [g(x) for x in lst]
def g(x)    : return float('%.4f' % x) 
"""

### More interesting, low-level stuff

"""
def timing(f,repeats=10):
  "How long does 'f' take to run?"
  import time
  time1 = time.clock()
  for _ in range(repeats):
    f()
  return (time.clock() - time1)*1.0/repeats

def showd(d):
  "Pretty print a dictionary."
  def one(k,v):
    if isinstance(v,list):
      v = gs(v)
    if isinstance(v,float):
      return ":%s %g" % (k,v)
    return ":%s %s" % (k,v)
  return ' '.join([one(k,v) for k,v in
                    sorted(d.items())
                     if not "_" in k])




####################################

## high-level business knowledge
def effort(d,project, a=2.94,b=0.91):
  "Primitive estimation function"
  def sf(x) : return x[0].isupper()
  sfs , ems = 0.0, 1.0
  kloc = project[d.kloc]
  i = -1
  for name,val in zip(d.names,project):
    i += 1
    if i > d.sfem : break
    if sf(name):
      sfs += val 
    else:
      ems *=  val
  return a*kloc**(b + 0.01*sfs) * ems

def cart(train,test,most):
  from sklearn import tree
  indep = map(lambda x: x[:most+1], train)
  dep   = map(lambda x: x[most+1],  train)
  t     = tree.DecisionTreeRegressor(random_state=1).fit(indep,dep)
  return t.predict(test[:most+1])[0]

def nc(n):
  return True #say(chr(ord('a') + n))
def loo(s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,
        s12,s13,s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24,s25,s26,
        s27,s28,s29,s30,s31,s32,s33,s34,s35,s36,s37,s38,s39,s40,s41,
        s42,s43,s44,s45,s46,s47,s48,s49,
        model=nasa93,t=tunings(),opt=None,detuning=True
        ):
  "Leave one-out"
  if opt == None: opt=options()
  d= model(opt)
  for i,project in enumerate(d.projects):
    want = project[d.effort]
    them = d.projects[:i] + d.projects[i+1:]
    if s15.use:
      nc(15)
      got15=knn(model(),them,project,opt,5); s15.seen(got15,want)
    if s16.use:
      nc(16)
      got16=knn(model(),them,project,opt,3); s16.seen(got16,want)
    if s17.use:
      nc(17)
      got17=knn(model(),them,project,opt,1); s17.seen(got17,want)
    #say(0)
    if s5.use or s7.use: 
      nc(5)
      got5,got7  = vasil(model,them,project); s5.seen(got5,want); s7.seen(got7,want)
    #say(1)
    if s1.use:
      nc(1)
      got1  = wildGuess(d,them,opt); s1.seen(got1,want)
    #say(2)
    if s4.use:
      nc(4)
      got4  = cart(them, project,d.kloc); s4.seen(got4,want)
    #say(5)
    if s8.use:
      nc(8)
      got8  = loc(d,them,project,3);     s8.seen(got8,want)
    if s18.use:
      nc(18)
      got18 = loc(d,them,project,1);     s18.seen(got18,want)
    #say(6)
    if s9.use or s10.use or s19.use or s20.use or s21.use or s22.use:
      project1 = project[:]
      project1[d.kloc]=0
      them1=[]
      for one in them: 
        tmp=one[:]
        tmp[d.kloc]=0
        them1 += [tmp]
      if s9.use or s10.use:
        nc(9)
        got9,got10  = vasil(model,them1,project1);
        s9.seen(got9,want); s10.seen(got10,want)
      if s19.use:
        nc(19)
        got19=knn(model(),them1,project1,opt,5); s19.seen(got19,want)
      if s20.use:
        nc(20)
        got20=knn(model(),them1,project1,opt,3); s20.seen(got20,want)
      if s21.use:
        nc(21)
        got21=knn(model(),them1,project1,opt,1); s21.seen(got21,want)
      if s22.use:
        nc(22)
        got22=cart(them1, project1,d.kloc);s22.seen(got22,want)

  if s2.use or s3.use:
    d= model(opt)
    d = valued(d,opt)
    for i,project in enumerate(d.projects):     
      want = project[d.effort]
      them = d.projects[:i] + d.projects[i+1:]
      if s2.use:
        nc(2)
        got2 = effort(d,project,2.94,0.91);   s2.seen(got2,want)
      if s3.use:
        nc(3)
        a,b  = coconut(d,them,opt);           
        got3 = effort(d,project,a,b);          s3.seen(got3,want)

  if s11.use or s12.use:
    #if not detuning: return True
    t=rrs3(tunings())
    d=model()
    d = valued(d,opt,t=t)
    for i,project in enumerate(d.projects):
      want= project[d.effort]
      them= d.projects[:i] + d.projects[i+1:]
    #say(7)
      if s11.use:
        nc(11)
        got11=effort(d,project,2.94,0.91); s11.seen(got11,want)
      if s12.use:
        nc(12)
        a,b=coconut(d,them,opt)
    #say(8)
        got12= effort(d,project,a,b); s12.seen(got12,want)
  if s23.use or s24.use or s25.use or s26.use:
     t = rrs3(tunings())
     d = model()
     d = valued(d,opt,t=t)
     for i,project in enumerate(d.projects):
       want= project[d.effort]
       them= d.projects[:i] + d.projects[i+1:]
       for n,s in [(8,s23), (12,s24), (16,s25),(4,s26)]:
         nc(23)
         them = shuffle(them)[:n]
         a,b = coconut(d,them,opt)
         got = effort(d,project,a,b); s.seen(got,want)
  if s27.use or s28.use or s29:
     for n,s in [(1,s27),(2,s28),(3,s29)]:
       t = rrs3(tunings())
       d = model()
       d = less(d,n)
       d = valued(d,opt,t=t)
       for i,project in enumerate(d.projects):
         nc(28)
         want= project[d.effort]
         them= d.projects[:i] + d.projects[i+1:]
         a,b = coconut(d,them,opt)
         got = effort(d,project,a,b); s.seen(got,want)
  if s30.use or s31.use or s32.use or s33.use or s34.use or s35.use or s36.use or s37.use or s38.use or s39.use or s40.use or s41.use:
     for n1,n2,s in [(0.25,4,s30),(0.25,8,s31),(0.25,12,s32),(0.25,16,s33),
                     (0.5, 4,s34),(0.5, 8,s35),(0.5, 12,s36),(0.5, 16,s37),
                     (1,4,s38),(1,8,s39),(1,12,s40),(1,16,s41)]:
       t = rrs3(tunings())
       d = model()
       d.projects = shuffle(d.projects)[:n2]
       d = fss(d,n1)
       d = valued(d,opt,t=t)
       for i,project in enumerate(d.projects):
         nc(36)
         want= project[d.effort]
         them= d.projects[:i] + d.projects[i+1:]
         a,b = coconut(d,them,opt)
         got = effort(d,project,a,b); s.seen(got,want)
    
  if  s13.use or s14.use:
    t=rrs5(tunings())
    d=model()
    d = valued(d,opt,t=t)
    for i,project in enumerate(d.projects):
      want= project[d.effort]
      them= d.projects[:i] + d.projects[i+1:]
    #say(9)
      if s13.use:
        nc(13)
        got13=effort(d,project,2.94,0.91); s13.seen(got13,want)
      if s14.use:
        nc(14)
        a,b=coconut(d,them,opt)
    #say("+")
        got14= effort(d,project,a,b); s14.seen(got14,want)

  if s42.use or s43.use or s44.use or s45.use or s46.use or s47.use or s48.use or s49.use:
     n1 = 0.5
     n2 = 8
     for noise,(carts,cocs,nuts,nears) in [
         (.25, (  s42, s44, s46, s48)),
         (.5, (  s43,  s45,s47, s49))
         ]:
       t = rrs3(tunings())
       d = model()
       d.projects = shuffle(d.projects)[:n2]
       d = fss(d,n1)
       d = valued(d,opt,t=t)
       for project in d.projects:
           old = project[d.kloc]
           new = old * ((1 - noise) + 2*noise*random.random())
           project[d.kloc]= new
       for i,project in enumerate(d.projects):
         nc(42)
         want= project[d.effort]
         them= d.projects[:i] + d.projects[i+1:]
         a,b=coconut(d,them,opt)
         nuts.seen(effort(d,project,a,b)      ,want)
         carts.seen(cart(them, project,d.kloc),want)
         cocs.seen(effort(d,project)          ,want)
        
         

def loc(d,them,project,n):
  me = project[d.kloc]
  all= sorted([(abs(me-x[d.kloc]),x[d.effort]) for x in them])
  one = two = three = four = five = all[0][1]
  if len(them) > 1: two = all[1][1]
  if len(them) > 2: three=all[2][1]
  if len(them) > 3: four=all[3][1]
  if len(them) > 4: five=all[4][1]
  # look at that: mean works as well as triangular kernel
  if n == 1 : return one
  if n == 2 : return (one *2 + two*1)/3
  if n == 3 : return  (one*3 + two*2+ three*1)/6
  if n == 4 : return (one * 4 + two * 3 + three * 2  + four * 1)/10
  return (one*5 + two*4 + three*3 + four*2 + five*1)/15
#  if n == 1 : return one
#  if n == 2 : return (one *1 + two*1)/2
#  if n == 3 : return  (one*1 + two*1+ three*1)/3
#  if n == 4 : return (one * 1 + two * 1 + three * 1  + four * 1)/4
#  return (one*1 + two*1 + three*1 + four*1 + five*1)/5

def walk(lst):
  lst = sorted([(median(x[1].all),x[0],x[1].all) for x in lst])
  say( lst[0][1])
  walk1(lst[0],lst[1:])
  print ""

def walk1(this,those):
  if those:
    that=those[0]
    _,n1=this[1], this[2]
    w2,n2=that[1], that[2]
    if mwu(n1,n2) :
      say(" < "+ str(w2))
      walk1(that,those[1:])
    else:
      say(" = " + str(w2))
      walk1(("","",n1+n2),those[1:])

def a12slow(lst1,lst2,rev=True):
  "how often is x in lst1 more than y in lst2?"
  more = same = 0.0
  for x in lst1:
    for y in lst2:
      if   x==y : same += 1
      elif rev     and x > y : more += 1
      elif not rev and x < y : more += 1
  x= (more + 0.5*same) / (len(lst1)*len(lst2))
  #if x > 0.71: return g(x),"B"
  #if x > 0.64: return g(x),"M"
  return x> 0.6 #g(x),"S"

def a12cmp(x,y):
  if y - x > 0 : return 1
  if y - x < 0 : return -1
  else: return 0

a12s=0
def a12(lst1,lst2, gt= a12cmp):
  "how often is x in lst1 more than y in lst2?"
  global a12s
  a12s += 1
  def loop(t,t1,t2): 
    while t1.j < t1.n and t2.j < t2.n:
      h1 = t1.l[t1.j]
      h2 = t2.l[t2.j]
      h3 = t2.l[t2.j+1] if t2.j+1 < t2.n else None 
      if gt(h1,h2) < 0:
        t1.j  += 1; t1.gt += t2.n - t2.j
      elif h1 == h2:
        if h3 and gt(h1,h3) < 0:
            t1.gt += t2.n - t2.j  - 1
        t1.j  += 1; t1.eq += 1; t2.eq += 1
      else:
        t2,t1  = t1,t2
    return t.gt*1.0, t.eq*1.0
  #--------------------------
  lst1 = sorted(lst1, cmp=gt)
  lst2 = sorted(lst2, cmp=gt)
  n1   = len(lst1)
  n2   = len(lst2)
  t1   = Thing(l=lst1,j=0,eq=0,gt=0,n=n1)
  t2   = Thing(l=lst2,j=0,eq=0,gt=0,n=n2)
  gt,eq= loop(t1, t1, t2)
  #print gt,eq,n1,n2
  return gt/(n1*n2) + eq/2/(n1*n2)


class Counts(): # Add/delete counts of numbers.
  def __init__(i,inits=[]):
    i.n = i.mu = i.m2 = 0.0
    for number in inits: i + number 
  def sd(i) : 
    if i.n < 2: return i.mu
    else:       
      return (i.m2*1.0/(i.n - 1))**0.5
  def __add__(i,x):
    i.n  += 1
    delta = x - i.mu
    i.mu += delta/(1.0*i.n)
    i.m2 += delta*(x - i.mu)
  
def wildGuess(d,projects,opt):
  tally = 0
  for _ in xrange(opt.guesses):
    project = any(projects)
    tally += project[d.effort]
  return tally*1.0/opt.guesses


def coconut(d,tests,opt,lvl=None,err=10**6,
            a=10,b=1,ar=10,br=0.5):
  "Chase good  a,b settings"
  #return 2.94,0.91
  def efforts(a,b):
    s=Score()
    for project in tests:
      got = effort(d,project,a,b)
      want = project[d.effort]
      s.seen(got,want)
    return s.mmre()
  if lvl == None: lvl=opt.levels
  if lvl < 1 : return a,b
  old = err
  for _ in range(opt.samples):
    a1 = a - ar + 2*ar*r()
    b1 = b - br + 2*br*r()
    tmp = efforts(a1,b1)
    if tmp < err:
      a,b,err = a1,b1,tmp
  if (old - err)/old < opt.epsilon:
    return a,b
  else:
    return coconut(d,tests,opt,lvl-1,err, a=a,b=b,
                   ar=ar*opt.shrink,
                   br=br*opt.shrink)

## sampple main
def main(model=nasa93):
  xseed(1)
  for shrink in [0.66,0.5,0.33]:
    for sam in [5,10,20]:
      for lvl in [5,10,20]:
        for rnd in [0,1,2]:
          opt=options()
          opt.shrink=shrink
          opt.samples=sam
          opt.round = rnd
          opt.levels = lvl
          loo(model=model,opt=opt)


#########################################
# start up code


def mwu(l1,l2):
  import numpy as np
  from scipy.stats import  mannwhitneyu
  #print "l1>",map(g,sorted(l1))
  #print "l2>",map(g,sorted(l2))
  _, p_value =  mannwhitneyu(np.array(l1), 
                             np.array(l2))
  return p_value <= 0.05

# for e in [1,2,4]:
#   print "\n"
#   l1 = [r()**e for _ in xrange(100)]
#   for y in [1.01,1.1,1.2,1.3,1.4, 1.5]:
#     l2 = map(lambda x: x*y,l1)
#     print e,y,mwu(l1,l2)

def test1(repeats=10,models=[coc81],what='locOrNot'):
  seed(1)
  print repeats,what,map(lambda x:x.__name__,models)
#for m in [ newCIIdata, xyz14,nasa93,coc81]:
  import time
  detune=False
  for m  in models:  
     #(newCIIdataDeTune,True),#, #, 
#     (xyz14deTune,True)
 #    #(coc81,True),
     #(nasa93,True)
  #  ]:
      s1=Score();  s2=Score(); s3=Score(); s4=Score();
      s5=Score();  s6=Score(); s7=Score(); s8=Score()
      s9=Score();  s10=Score(); s11=Score(); s12=Score();
      s13=Score(); s14=Score();
      s15=Score();  s16=Score(); s17=Score(); s18=Score()
      s19=Score();  s20=Score(); s21=Score();
      s22=Score()
      s23=Score()
      s24=Score(); s25=Score(); s26=Score()
      s27=Score(); s28=Score(); s29=Score()
      s30=Score(); s31=Score(); s32=Score()
      s33=Score(); s34=Score(); s35=Score()
      s36=Score(); s37=Score(); s38=Score()
      s39=Score(); s40=Score(); s41=Score()

      s42=Score(); s43=Score(); s44=Score()
      s45=Score(); s46=Score(); s47=Score()
      s48=Score(); s49=Score();
      # loc or no loc
      exps =dict(locOrNot = [("coc2000",s2),("coconut",s3),
                             ("loc(3)",s8), ("loc(1)",s18), 
                             #('knear(3)',s16),  ("knear(3) noloc",s20),
                             #('knear(1)',s17),("knear(1) noloc",s21) 
                             ],
                 basicRun = [("coc2000",s2),("coconut",s3),
                             ('knear(3)',s16),('knear(1)',s17),
                             #("cluster(1)",s5),
                             ("cluster(2)",s7),   
                             ("cart",s4)],
                 qualitative= [("coc2000",s2),("coconut",s3),
                               #('knear(3)',s16),('knear(1)',s17),
                               ("coco2000(simp)",s13), ("coconut(simp)",s14),
                               ("coco2000(lmh)",s11), ("coconut(lmh)",s12)],
                 other    =  [('(c=1)n-noloc',s9),('(c=2)n-noloc',s10)],
                 less     = [("coc2000",s2),("coconut",s3),
                             ("coco2000(lmh)",s11), ("coconut(lmh)",s12),
                             ('coconut(lmh8)',s23),('coconut(lmh12)',s24), 
                             ('coconut(lmh16)',s25),
                             ('coconut(lmh4)',s26)],
                 lessCols = [("coc2000",s2),("coconut",s3),
                             ('coconut(just5)',s27),
                             ('coconut(just10)',s28),
                             ('coconut(just15)',s29)],
                 fssCols = [("coc2000",s2),("coconut",s3),
                            ('coconut:c*0.25,r=4',s30),
                            ('coconut:c*0.25,r=8',s31),
                            #('coconut:c*0.25,r=12',s32),
                            #('coconut:c*0.25,r=16',s33),
                            ('coconut:c*0.5,r=4',s34),
                            ('coconut:c*0.5,r=8',s35),
                            #('coconut:c*0.5,r=12',s36),
                            #('coconut:c*1,r=16',s37),
                            ('coconut:c*1,r=4',s38),
                            ('coconut:c*1,r=8',s39),
                            #('coconut:c*1,r=12',s40),
                            #('coconut:c*1,r=16',s41)
                          ],
                  noise = [  ("cart",s4),               ("cart/4",s42),               ("cart/2",s43),         
                             ("coc2000",s2),            ("coc2000n/4",s44),           ("coc2000n/2",s45),
                             ('coconut:c*0.5,r=8',s35), ('coconut:c*0.5r=8n/4',s46) , ('coconut:c*0.5,r=8n/2',s47),
                             ('knear(1)',s17),          ('knear(1)/4',s48),           ('knear(1)/2',s49)
                           ]
                 )
      lst = exps[what]
      print '%',what
      for _,s in lst: s.use=True
      t1=time.clock()
      print "\n\\subsection{%s}" % m.__name__
      say("%")
      for i in range(repeats):

        say(' ' + str(i))
        loo(s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,
            s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24,s25,s26,
             s27,s28,s29,s30,s31,s32,
            s33,s34,s35,s36,s37,s38,s39,s40,s41,s42,s43,s44,s45,s46,s47,s48,s49,
            model=m,detuning=detune)
      global bs
      global a12s
      bs = a12=0
      t2 = time.clock()
      print "="
      rdivDemo([[x[0]] + x[1].all for x in lst if x[1].all])
      t3 = time.clock()
      print "\n :learn",t2-t1,":analyze",t3-t2,":boots",bs,"effects",a12s,":conf",0.99**bs
      
#print 'B>', bootstrap([1,2,3,4,5],[1,2,3,4,5])

def knn(src,them,project,opt,k):
  slots = where0(what= lambda x:cocVals(x,src.effort))
  m0=Model(src.names,src.projects)
  m1=clone(m0,them)
  w = [None]*k
  ws = 0
  for i in range(k): ws += i+1
  for i in range(k): w[i] = (i+1)/ws
  w.reverse()
  #w = [1/k]*k
  
  dists =[(dist(m1,Row(cells=that),Row(cells=project),slots),that[src.effort])
          for that in them]
  est = 0
  for w1,(_,x) in zip(w,sorted(dists)[:k]):
    est += w1*x
  return est

def cocVals(row,n):
  if isinstance(row,Row):
    row=row.cells
  return row[:n]

def vasil(src,data,project):
  all = src()
  m0 = Model(all.names,all.projects)
  m1 = clone(m0,data)
  e  = all.effort
  slots = where0(what= lambda x:cocVals(x,e)
                 ,klass=lambda x:x.cells[all.effort])
  t     = where(m1,m1.rows,slots)
  row = Row(cells=project)
  got1 = got2 = Num(slots.klass(r) for r in data).median()
  (d1,c1),(d2,c2) = centroid2(row,t)
  if c1 or c2:
    w1,w2 = 1/(d1+0.0001), 1/(d2+0.0001)
    e1 = c1.m.centroid()[e]
    e2 = c2.m.centroid()[e]
    got2 = (w1*e1 + w2*e2) / (w1+w2)
    got1=myCentroid(row,t).m.centroid()[e]
  #got1b=leaf(t,row,slots).m.centroid()[e]
  return got1,got2

class Num:
  "An Accumulator for numbers"
  def __init__(i,name,inits=[]): 
    i.n = i.m2 = i.mu = 0.0
    i.all=[]
    i._median=None
    i.name = name
    i.rank = 0
    for x in inits: i.add(x)
  def s(i)       : return (i.m2/(i.n - 1))**0.5
  def add(i,x):
    i._median=None
    i.n   += 1   
    i.all += [x]
    delta  = x - i.mu
    i.mu  += delta*1.0/i.n
    i.m2  += delta*(x - i.mu)
  def __add__(i,j):
    return Num(i.name + j.name,i.all + j.all)
  def quartiles(i):
    def p(x) : return int(100*g(xs[x]))
    i.median()
    xs = i.all
    n  = int(len(xs)*0.25)
    return p(n) , p(2*n) , p(3*n)
  def median(i):
    if not i._median:
      i.all = sorted(i.all)
      i._median=median(i.all)
    return i._median
  def __lt__(i,j):
    return i.median() < j.median() 
  def spread(i):
    i.all=sorted(i.all)
    n1=i.n*0.25
    n2=i.n*0.75
    if len(i.all) <= 1:
      return 0
    if len(i.all) == 2:
      return i.all[1] - i.all[0]
    else:
      return i.all[int(n2)] - i.all[int(n1)]


def different(l1,l2):
  #return bootstrap(l1,l2) and a12(l2,l1)
  return a12(l2,l1) and bootstrap(l1,l2)


def scottknott(data,cohen=0.3,small=3, useA12=False,epsilon=0.01):
  """Recursively split data, maximizing delta of
  the expected value of the mean before and 
  after the splits. 
  Reject splits with under 3 items"""
  #data = [d for d in data if d.spread() < 0.75]
  all  = reduce(lambda x,y:x+y,data)
  #print sorted(all.all)
  same = lambda l,r: abs(l.median() - r.median()) <= all.s()*cohen
  if useA12: 
    same = lambda l, r:   not different(l.all,r.all) 
  big  = lambda    n: n > small    
  return rdiv(data,all,minMu,big,same,epsilon)

def rdiv(data,  # a list of class Nums
         all,   # all the data combined into one num
         div,   # function: find the best split
         big,   # function: rejects small splits
         same, # function: rejects similar splits
         epsilon): # small enough to split two parts
  """Looks for ways to split sorted data, 
  Recurses into each split. Assigns a 'rank' number
  to all the leaf splits found in this way. 
  """
  def recurse(parts,all,rank=0):
    "Split, then recurse on each part."
    cut,left,right = maybeIgnore(div(parts,all,big,epsilon),
                                 same,parts)
    if cut: 
      # if cut, rank "right" higher than "left"
      rank = recurse(parts[:cut],left,rank) + 1
      rank = recurse(parts[cut:],right,rank)
    else: 
      # if no cut, then all get same rank
      for part in parts: 
        part.rank = rank
    return rank
  recurse(sorted(data),all)
  return data

def maybeIgnore((cut,left,right), same,parts):
  if cut:
    if same(sum(parts[:cut],Num('upto')),
            sum(parts[cut:],Num('above'))):    
      cut = left = right = None
  return cut,left,right

def minMu(parts,all,big,epsilon):
  """Find a cut in the parts that maximizes
  the expected value of the difference in
  the mean before and after the cut.
  Reject splits that are insignificantly
  different or that generate very small subsets.
  """
  cut,left,right = None,None,None
  before, mu     =  0, all.mu
  for i,l,r in leftRight(parts,epsilon):
    if big(l.n) and big(r.n):
      n   = all.n * 1.0
      now = l.n/n*(mu- l.mu)**2 + r.n/n*(mu- r.mu)**2  
      if now > before:
        before,cut,left,right = now,i,l,r
  return cut,left,right

def leftRight(parts,epsilon=0.01):
  """Iterator. For all items in 'parts',
  return everything to the left and everything
  from here to the end. For reasons of
  efficiency, take a first pass over the data
  to pre-compute and cache right-hand-sides
  """
  rights = {}
  n = j = len(parts) - 1
  while j > 0:
    rights[j] = parts[j]
    if j < n: rights[j] += rights[j+1]
    j -=1
  left = parts[0]
  for i,one in enumerate(parts):
    if i> 0: 
      if parts[i]._median - parts[i-1]._median > epsilon:
        yield i,left,rights[i]
      left += one

bs=0
def bootstrap(y0,z0,conf=0.01,b=1000):
  """The bootstrap hypothesis test from
     p220 to 223 of Efron's book 'An
    introduction to the boostrap."""
  global bs
  bs += 1
  class total():
    "quick and dirty data collector"
    def __init__(i,some=[]):
      i.sum = i.n = i.mu = 0 ; i.all=[]
      for one in some: i.put(one)
    def put(i,x):
      i.all.append(x);
      i.sum +=x; i.n += 1; i.mu = float(i.sum)/i.n
    def __add__(i1,i2): return total(i1.all + i2.all)
  def testStatistic(y,z): 
    """Checks if two means are different, tempered
     by the sample size of 'y' and 'z'"""
    tmp1 = tmp2 = 0
    for y1 in y.all: tmp1 += (y1 - y.mu)**2 
    for z1 in z.all: tmp2 += (z1 - z.mu)**2
    s1    = (float(tmp1)/(y.n - 1))**0.5
    s2    = (float(tmp2)/(z.n - 1))**0.5
    delta = z.mu - y.mu
    if s1+s2:
      delta =  delta/((s1/y.n + s2/z.n)**0.5)
    return delta
  def one(lst): return lst[ int(any(len(lst))) ]
  def any(n)  : return random.uniform(0,n)
  y, z   = total(y0), total(z0)
  x      = y + z
  tobs   = testStatistic(y,z)
  yhat   = [y1 - y.mu + x.mu for y1 in y.all]
  zhat   = [z1 - z.mu + x.mu for z1 in z.all]
  bigger = 0.0
  for i in range(b):
    if testStatistic(total([one(yhat) for _ in yhat]),
                     total([one(zhat) for _ in zhat])) > tobs:
      bigger += 1
  return bigger / b < conf

def bootstrapd(): 
  def worker(n=30,mu1=10,sigma1=1,mu2=10.2,sigma2=1):
    def g(mu,sigma) : return random.gauss(mu,sigma)
    x = [g(mu1,sigma1) for i in range(n)]
    y = [g(mu2,sigma2) for i in range(n)]
    return n,mu1,sigma1,mu2,sigma2,\
        'different' if bootstrap(x,y) else 'same'
  print worker(30, 10.1, 1, 10.2, 1)
  print worker(30, 10.1, 1, 10.8, 1)
  print worker(30, 10.1, 10, 10.8, 1)
 

def rdivDemo(data,max=100):
  def z(x):
    return int(100 * (x - lo) / (hi - lo + 0.00001))
  data = map(lambda lst:Num(lst[0],lst[1:]),
             data)
  print ""
  ranks=[]
  for x in scottknott(data,useA12=True):
    ranks += [(x.rank,x.median(),x)]
  all=[]
  for _,__,x in sorted(ranks):
    all += x.quartiles()
  all = sorted(all)
  lo, hi = all[0], all[-1]
  print "{\\scriptsize \\begin{tabular}{l@{~~~}l@{~~~}r@{~~~}r@{~~~}c}"
  print "\\arrayrulecolor{darkgray}"
  print '\\rowcolor[gray]{.9}  rank & treatment & median & IQR & \\\\' #min= %s, max= %s\\\\' % (int(lo),int(hi))
  last = None
  for _,__,x in sorted(ranks):
    q1,q2,q3 = x.quartiles()
    pre =""
    if not last == None and not last == x.rank:
      pre= "\\hline"
    print pre,'%2s & %12s &    %s  &  %s & \quart{%s}{%s}{%s}{%s} \\\\' % \
        (x.rank+1, x.name, q2, q3 - q1, z(q1), z(q3) - z(q1), z(q2),z(100))
    last = x.rank 
  print "\\end{tabular}}"

def rdiv0():
  rdivDemo([
        ["x1",0.34, 0.49, 0.51, 0.6],
        ["x2",6,  7,  8,  9] ])

def rdiv1():
  rdivDemo([
        ["x1",0.1,  0.2,  0.3,  0.4],
        ["x2",0.1,  0.2,  0.3,  0.4],
        ["x3",6,  7,  8,  9] ])

def rdiv2():
  rdivDemo([
        ["x1",0.34, 0.49, 0.51, 0.6],
        ["x2",0.6,  0.7,  0.8,  0.9],
        ["x3",0.15, 0.25, 0.4,  0.35],
        ["x4",0.6,  0.7,  0.8,  0.9],
        ["x5",0.1,  0.2,  0.3,  0.4] ])

def rdiv3():
  rdivDemo([
      ["x1",101, 100, 99,   101,  99.5],
      ["x2",101, 100, 99,   101, 100],
      ["x3",101, 100, 99.5, 101,  99],
      ["x4",101, 100, 99,   101, 100] ])

def rdiv4():
  rdivDemo([
      ["1",11,12,13],
      ["2",14,31,22],
      ["3",23,24,31],
      ["5",32,33,34]])

def rdiv5():
  rdivDemo([
      ["1",11,11,11],
      ["2",11,11,11],
      ["3",11,11,11]])

def rdiv6():
  rdivDemo([
      ["1",11,11,11],
      ["2",11,11,11],
      ["4",32,33,34,35]])

#rdiv0(); rdiv1(); rdiv2(); rdiv3(); rdiv4(); rdiv5(); rdiv6()
#exit() 


repeats=10
exp='locOrNot'
models=['newCIIdataDeTune',
         'xyz14deTune'
         'coc81',
          'nasa93']
if len(sys.argv)>=2:
  repeats=eval(sys.argv[1])
if len(sys.argv)>=3:
  exp=sys.argv[2]
if len(sys.argv)>3:
  models=sys.argv[3:]

test1(repeats=repeats,models=map(eval,models),what=exp)


