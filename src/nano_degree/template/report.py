def outputHTML(arg):
   text_file = open("webserver/output/report.html", "w")
   text_file.write("<h1>Report</h1>")
   text_file.write("<p>%s</p>" % arg)
   text_file.close()