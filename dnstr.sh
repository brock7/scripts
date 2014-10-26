dig ns $1 | awk "
	found == 1 && match(\$1,\"$1\"){ 
		if (NF == 5) {
			print \$5;
			sub(\".\$\", \"\", \$5);
			system(\"dig axfr @\"\$5\" $1\");
		}
	} 
	/ANSWER SECTION:/{found = 1}"

