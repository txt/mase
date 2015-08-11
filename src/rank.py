
def rank_simple(vector):
    return sorted(range(len(vector)), key=vector.__getitem__)

def rankdata(a):
    n = len(a)
    ivec=rank_simple(a)
    svec=[a[rank] for rank in ivec]
    sumranks = 0
    dupcount = 0
    newarray = [0]*n
    for i in xrange(n):
        sumranks += i
        dupcount += 1
        if i==n-1 or svec[i] != svec[i+1]:
            averank = sumranks / float(dupcount) + 1
            for j in xrange(i-dupcount+1,i+1):
                newarray[ivec[j]] = averank
            sumranks = 0
            dupcount = 0
    return newarray


print(rankdata([3, 1, 4, 15, 92]))
# [2.0, 1.0, 3.0, 4.0, 5.0]
print(rankdata([1, 2, 3, 3, 3, 4, 5]))

# [1.0, 2.0, 4.0, 4.0, 4.0, 6.0, 7.0]

print(rankdata([1, 2, 3, 3, 3, 4, 5]))

 function mwu(pop1,pop2,up,critical,                 \
	      i,data,ranks,n,n1,sum1,ranks1,n2,sum2,ranks2, \
	      correction,meanU,sdU,z) 
 {   # returns true if the pops are the same
     for(i in pop1) data[++n]=pop1[i]
     for(i in pop2) data[++n]=pop2[i]
     rank(data,ranks)
     for(i in pop1) { n1++; sum1 += ranks1[i] = ranks[pop1[i]] }
     for(i in pop2) { n2++; sum2 += ranks2[i] = ranks[pop2[i]] }
     meanU      = n1*(n1+n2+1)/2;  # symmetric, just use pop1's z
     sdU        = (n1*n2*(n1+n2+1)/12)^0.5
     correction = sum1 > meanU ? -0.5 : 0.5  
     z          = abs((sum1 - meanU + correction )/sdU)
     return  (z >= 0 && z <= critical) 
 }
