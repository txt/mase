  BEGIN	   {  
	 q="\""
	 First = 1      
	 In = 1
  }
  /^"""</,/^>"""/ {  next } 
  /^"""/	  {  Once = 1
                     In = 1 - In       
		     if (In) 
		       print "````python"
		     else	  
		       if (First)   
			 First = 0   
		       else     
			 print "````"  
		     next }       
  ! First {  pre = In ? sprintf("% 4s: ",++line) : ""
             print $0 }       
  END     { if (In ) print "````"
            if (!Once) print "```"  
}
