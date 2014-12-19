#!/usr/bin/python

# Simple Log File Analyzer by Valentin Hoebel
# Version 1.0 (6th June 2010)

# Contact me at valentin@xenuser.org
# Website: I am sure you will find me! :)
# ASCII FOR BREAKFAST

# Description:
# This tool helps you to find hack attempts
# within webserver log files (e.g. Apache2 access logs).

# Features:
# - Error handling
# - Scan a log file for four different attack types
# - Display a short scan report
# - Write scan results to a new log file
# - Easy to use (everything is simple and automated

# Usage example:
# scan_log.py -file vhost_access.log

# Known issue:
# XSS attempt discovery feature can be a little bit buggy.

# Tested with:
# Apache2 log files only. Sry guys! But I am sure
# that every other webserver log file will work aswell.

# Disclaimer:
# I am not responsible if this script or you cause any damage
# to your system. The memory consumption can become
# quite large and the generated reports very huge. So be sure
# you know what you are doing. I highly recommend you
# download your log files on a separate machine and
# analyze these files there.

# I know that there are much better tools, but well, I do
# this for learning and fun =)

# Attention: Tool is far away from being perfect, so don't rely a 100 percent on it.

# A BIG "Thank you!" to all who publish their awesome Python
# scripts online and help other ppl learning this language.

# Modify, distribute, share and copy this code in any way you like!

# Power to the cows!

import sys, string, re, time
from time import strftime, localtime

def print_usage():
    print ""
    print ""
    print "________________________________________________"
    print "Simple Log File Analyzer"
    print "by Valentin Hoebel (valentin@xenuser.org)"
    print ""
    print "Version 1.0 (6th June 2010)   ^__^"
    print "                              (oo)\________"
    print "                              (__)\        )\/\ "
    print "                                  ||----w |"
    print "Power to teh cows!                ||     ||"
    print "________________________________________________"
    print ""
    print "[!] Use parameter --help for help!"
    print ""
    print ""
    return
    
def print_help():
    print ""
    print ""
    print "________________________________________________"
    print "Simple Log File Analyzer"
    print "by Valentin Hoebel (valentin@xenuser.org)"
    print ""
    print "Version 1.0 (6th June 2010)   ^__^"
    print "                              (oo)\________"
    print "                              (__)\        )\/\ "
    print "                                  ||----w |"
    print "Power to teh cows!                ||     ||"
    print "________________________________________________"
    print ""
    print "The Simple Log File Analyzer helps you to find"
    print "common hack attempts within your webserver log."
    print ""
    print "Supported attacks:"
    print " - SQL Injection"
    print " - Local File Inclusion"
    print " - Remote File Inclusion"
    print " - Cross-Site Scripting"
    print ""
    print "This scanner doesn't find everything so don't"
    print "rely on it!"
    print ""
    print "Usage example:"
    print "scan_log.py -file vhost_access.log"
    print ""
    print "Options:"
    print " -file <file>   (starts the main analyzing function"
    print " --help         (displays this text)"
    print ""
    print "Features:"
    print " - Error handling"
    print " - Scan a log file for four different attack types"
    print " - Display a short scan report"
    print " - Write scan results to a new log file"
    print " - Easy to use (everything is simple and automated)"
    print ""
    print "Additional information:"
    print "I only tested this tool with Apache2 log files (up to 2000 lines)."
    print "It may happen that the tool crashes when the provided log"
    print "file is too big or contains too many lines/characters."
    print "Scanning a 4000 lines log file only takes one second."
    print ""
    print "Hint: The XSS discovery feature is a little bit buggy."
    print ""
    print ""
    return
    
def print_banner():
    print ""
    print ""
    print "________________________________________________"
    print "Simple Log File Analyzer"
    print "by Valentin Hoebel (valentin@xenuser.org)"
    print ""
    print "Version 1.0 (6th June 2010)   ^__^"
    print "                              (oo)\________"
    print "                              (__)\        )\/\ "
    print "                                  ||----w |"
    print "Power to teh cows!                ||     ||"
    print "________________________________________________"
    return

# Define the function for analyzing log files
def analyze_log_file(provided_file):
    # Defining some important vars
    sqli_found_list = {}
    lfi_found_list = {}
    rfi_found_list = {}
    xss_found_list = {}
    
    # I know, there are better methods for doing/defining this...
    sql_injection_1 = "UNION"
    sql_injection_2 = "ORDER"
    sql_injection_3 = "GROUP"
        
    local_file_inclusion_1 = "/etc/passwd"
    local_file_inclusion_2 = "/etc/passwd%20"
    local_file_inclusion_3 = "=../"
    
    remote_file_inclusion_1 = "c99"
    remote_file_inclusion_2 = "=http://"
    
    cross_site_scripting_1 = "XSS"
    cross_site_scripting_2 = "alert"
    cross_site_scripting_3 = "String.fromCharCode"
    cross_site_scripting_4 = "iframe"
    cross_site_scripting_5 = "javascript"
    
    print "[i] >>",  provided_file
    print "[i] Assuming you provided a readable log file."
    print "[i] Trying to open the log file now."
    print ""

    # Opening the log file
    try:
        f = open(provided_file,  "r")
    except IOError:
        print "[!] The file doesn't exist."
        print "[!] Exiting now!"
        print ""
        sys.exit(1)
    
    print "[i] Opening the log file was successfull."
    print "[i] Moving on now..."
    print ""
    
    # Storing every single line in a list
    line_list = [line for line in f]
    max_lines = len(line_list)
    print "[i] The file contains", max_lines,  "lines."
    print "[i] Now looking for possible hack attempts..."
    
    # Viewing every single line
    for x in xrange(1, max_lines):
        current_line = line_list[x:x+1]
        
        # For some strange list behaviour we convert the list into a string
        current_line_string = "".join(current_line)
        
        # Search for SQL injections 
        find_sql_injection_1 =  re.findall(sql_injection_1, current_line_string) 
        if len(find_sql_injection_1) != 0:
            sqli_found_list[x+1] = current_line_string        
        else:
            find_sql_injection_2 = re.findall(sql_injection_2,  current_line_string)
            if len(find_sql_injection_2) != 0:
                sqli_found_list[x+1] = current_line_string
            else:
                find_sql_injection_3 = re.findall(sql_injection_3,  current_line_string)
                if len(find_sql_injection_3) != 0:
                    sqli_found_list[x+1] = current_line_string 
    
        # Search for local file inclusions
        find_local_file_inclusion_1 =  re.findall(local_file_inclusion_1, current_line_string) 
        if len(find_local_file_inclusion_1) != 0:
            lfi_found_list[x+1] = current_line_string        
        else:
            find_local_file_inclusion_2 = re.findall(local_file_inclusion_2,  current_line_string)
            if len(find_local_file_inclusion_2) != 0:
                lfi_found_list[x+1] = current_line_string
            else:
                find_local_file_inclusion_3 = re.findall(local_file_inclusion_3,  current_line_string)
                if len(find_local_file_inclusion_3) != 0:
                    lfi_found_list[x+1] = current_line_string
                    
        # Search for remote file inclusions
        find_remote_file_inclusion_1 =  re.findall(remote_file_inclusion_1, current_line_string) 
        if len(find_remote_file_inclusion_1) != 0:
            rfi_found_list[x+1] = current_line_string        
        else:
            find_remote_file_inclusion_2 = re.findall(remote_file_inclusion_2,  current_line_string)
            if len(find_remote_file_inclusion_2) != 0:
                rfi_found_list[x+1] = current_line_string

        # Search for cross-site scripting attempts
        find_cross_site_scripting_1 = re.findall(cross_site_scripting_1,  current_line_string)
        if len(find_cross_site_scripting_1) != 0:
            xss_found_list[x+1] = current_line_string
        else:
            find_cross_site_scripting_2 = re.findall(cross_site_scripting_2,  current_line_string)
            if len(find_cross_site_scripting_2) != 0:
                xss_found_list[x+1] = current_line_string
            else:
                find_cross_site_scripting_3 = re.findall(cross_site_scripting_3,  current_line_string)
                if len(find_cross_site_scripting_3) != 0:
                    xss_found_list[x+1] = current_line_string
                else:
                    find_cross_site_scripting_4= re.findall(cross_site_scripting_4,  current_line_string)
                    if len(find_cross_site_scripting_4) != 0:
                        xss_found_list[x+1] = current_line_string
                    else:
                        find_cross_site_scripting_5 = re.findall(cross_site_scripting_5,  current_line_string)
                        if len(find_cross_site_scripting_5) != 0:
                            xss_found_list[x+1] = current_line_string

    # Close the file we opened recently
    f.close() 

    # Generating a short report
    print "[i] Done."
    print ""
    print "[#] Simple report for analyzed log file"
   
    check_for_sqli_attempts = len(sqli_found_list)
    if check_for_sqli_attempts > 0:
        print "[!]", check_for_sqli_attempts,  "SQL injection attempt(s) was/were found."
    else:
        print "[+] No SQL injection attempt was found."
    
    check_for_lfi_attempts = len(lfi_found_list)
    if check_for_lfi_attempts > 0:
        print "[!]",  check_for_lfi_attempts,  "local file inclusion attempt(s) was/were found."    
    else:
        print "[+] No local file inclusion attempt was found." 
 
    check_for_rfi_attempts = len(rfi_found_list)
    if check_for_rfi_attempts > 0:
        print "[!]",  check_for_rfi_attempts,  "remote file inclusion attempt(s) was/were found."       
    else:
        print "[+] No remote file inclusion attempt was found." 
   
    check_for_xss_attempts = len(xss_found_list)
    if check_for_xss_attempts > 0:
        print "[!]",  check_for_xss_attempts,  "cross-site scripting attempt(s) was/were found."    
    else:
        print "[+] No crosse-site scripting attempt was found." 
    
    
    # Now generate the report
    print ""
    print "[i] Generating report..."
    
    # Define variables for the report name
    time_string = strftime("%a_%d_%b_%Y_%H_%M_%S", localtime())
    time_string_for_report = strftime("%a the %d %b %Y, %H:%M:%S", localtime())
    name_of_report_file = provided_file + "_scan_report_from_" + time_string
    
    # Convert the ints to strings
    sqli_numbers = str(check_for_sqli_attempts)
    lfi_numbers = str(check_for_lfi_attempts)
    rfi_numbers = str(check_for_rfi_attempts)
    xss_numbers = str(check_for_xss_attempts)
    
    # Create the file
    generated_report = open(name_of_report_file,  "w")
    
    # Write the content    
    generated_report.write("\n")
    generated_report.write("Simple Log File Analyzer\n")
    generated_report.write("by Valentin Hoebel (valentin@xenuser.org)\n")
    generated_report.write("\n")
    generated_report.write("Version 1.0 (6th June 2010)   ^__^\n")
    generated_report.write("                              (oo)\________\n")
    generated_report.write("                              (__)\        )\/\ \n")
    generated_report.write("                                  ||----w |\n")
    generated_report.write("Power to teh cows!                ||     ||\n")
    generated_report.write("________________________________________________\n")
    generated_report.write("\n")
    generated_report.write("Scan report for " +provided_file +  " on " + time_string_for_report + "\n")
    generated_report.write("Hint: XSS attempt discovery feature might be a little bit buggy.\n")
    generated_report.write("\n")
    generated_report.write("\n")
    generated_report.write("Number of possible SQL injection attempts found: " + sqli_numbers + "\n")
    generated_report.write("Number of possible local file inclusion attempts found: " + lfi_numbers + "\n")
    generated_report.write("Number of possible remote file inclusion attempts found: " + rfi_numbers + "\n")
    generated_report.write("Number of possible cross-site scripting attempts found: " + xss_numbers + "\n")
    generated_report.write("\n")
    generated_report.write("\n")
    if len(sqli_found_list) != 0:
        sqli_found_list_string = ""
        sqli_found_list_string = "".join(str(sqli_found_list))
        generated_report.write("Details for the SQL injection attempts (line, log entry)\n")
        generated_report.write("------------------------------------------------\n")
        generated_report.write(sqli_found_list_string)
        generated_report.write("\n")
        generated_report.write("\n")
        generated_report.write("\n")
    if len(lfi_found_list) != 0:
        lfi_found_list_string = ""
        lfi_found_list_string = "".join(str(lfi_found_list))
        generated_report.write("Details for the local file inclusion attempts (line, log entry)\n")
        generated_report.write("------------------------------------------------\n")
        generated_report.write(lfi_found_list_string)  
        generated_report.write("\n")
        generated_report.write("\n")
        generated_report.write("\n")
    if len(rfi_found_list) != 0:
        rfi_found_list_string = ""
        rfi_found_list_string = "".join(str(rfi_found_list))
        generated_report.write("Details for the remote file inclusion attempts (line, log entry)\n")
        generated_report.write("------------------------------------------------\n")
        generated_report.write(rfi_found_list_string) 
        generated_report.write("\n")
        generated_report.write("\n")
        generated_report.write("\n")
    if len(xss_found_list) != 0:
        xss_found_list_string = ""
        xss_found_list_string = "".join(str(xss_found_list))
        generated_report.write("Details for the cross-site scripting attempts (line, log entry)\n")
        generated_report.write("------------------------------------------------\n")
        generated_report.write(xss_found_list_string) 
        generated_report.write("\n")
        generated_report.write("\n")
        generated_report.write("\n") 
    
    # Close the file
    generated_report.close()
    print "[i] Finished writing the report."
    print "[i] Hint: The report file can become quite large."
    print "[i] Hint: The XSS attempt discovery feature might be a little bit buggy."
    print ""
    
    print "[i] That's it, bye!"
    print ""
    print ""
    return
    # End of the log file function
    
# Checking if argument was provided
if len(sys.argv) <=1:
    print_usage()
    sys.exit(1)
    
for arg in sys.argv:
    # Checking if help was called
    if arg == "--help":
        print_help()
        sys.exit(1)
    
    # Checking if  a log file was provided, if yes -> go!
    if arg == "-file":
        provided_file = sys.argv[2]
        print_banner()
        
        #  Start the main analyze function
        analyze_log_file(provided_file)
        sys.exit(1)
        
### EOF ###
