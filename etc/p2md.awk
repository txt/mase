  BEGIN	   {
	 q="\""
	 First = 1      
	 In = 1
  }
  /^"""</,/^>"""/ {  next } 
  /^"""/	  {  Once = 1
                     In = 1 - In       
		     if (In) {
                       start = NR
		     }
                     else	  
		       if (First)   
			 First = 0   
		       else   {  	 
			 
	                 print "<a href=\""name"#L"start+1"-L"NR-1"\"><img align=right src=\"http://www.hungarianreference.com/i/arrow_out.gif\"></a><br clear=all>"
                         print "```python"
                         print lines
                         lines=""
                         print "```"
                        }  
		     next }       
  ! First {  pre = In ? sprintf("% 4s:   ",++line) : ""
             line =  pre $0
             if (In) 
               lines = lines "\n" line
             else
               print line
          }
  END     {  if (In ) {
                  print "<a href=\""name"#L"start+1"-L"NR-1"\"><img align=right src=\"http://www.hungarianreference.com/i/arrow_out.gif\"></a><br clear=all>"
                         print "```python"
                         print lines
                         lines=""
                         print "```"
             }
            if (!Once) print "```"  
}
