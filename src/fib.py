def memo(f):
  memo = {}
  def helper(*lst,**d):
    if lst not in memo:            
      memo[lst] = f(*lst,**d)
    return memo[lst]
  return helper
    
@memo
def fib(n):
  return n if n < 2 else fib(n-1) + fib(n-2)

print fib(300)

