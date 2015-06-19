import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 

def lines(xlabel, ylabel, title, f="lines.png",
          xsize=5,ysize=5,lines=[]): 
  width = len(lines[0][1:])
  xs = [x for x in xrange(1,width+1)] 
  plt.figure(figsize=(xsize,ysize))
  plt.xlabel(xlabel)
  plt.ylabel(ylabel) 
  for line in lines: 
    plt.plot(xs,  line[1:],
                 label = line[0])
   
  plt.locator_params(nbins=len(xs))
  plt.title(title)
  plt.legend()
  plt.tight_layout()
  plt.savefig(f)
  
lines("days","production","Fruit output",
      xsize=3,ysize=3,lines=[
      ["apples",4,3,2,1],
      ["oranges",9,4,1,0.5]])
 