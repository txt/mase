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
  ! First {  pre = In ? sprintf("<font color=red>% 4s:</font> ",++line) : ""
             print pre $0 }       
  END     { if (In ) print "````"
            if (!Once) print "```"  
}
