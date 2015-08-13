  BEGIN	   {  
	 q="\""
	 First = 1      
	 In = 1
  }
  /^"""</,/^>"""/ {  next } 
  /^"""/	  {  Once = 1
                     In = 1 - In       
		     if (In) {
		       print "````python"
                       start = NR
		     }
                     else	  
		       if (First)   
			 First = 0   
		       else   {  
			 print "````"
                         print "<a href=\""name"#L"start"-L"NR"\">src</a>"
                        }  
		     next }       
  ! First {  pre = In ? sprintf("% 4s:   ",++line) : ""
             print pre $0 }       
  END     { if (In ) print "````"
            if (!Once) print "```"  
}
