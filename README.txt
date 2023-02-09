To reset the admin's password, run server.py to start the server, then webscraper.py to do the rest.
The password reset is handled automatically and the admin's new password is determined by the new_password variable.
Webscraper also has support for custom passwords via a commandline argument, to do this simply put your desired password after the executable to have it replace the admin's old password. For example, if the command to run the program is 'python3 .\webscraper.py', then to input a custom password simply do 'python3 .\webscraper.py custom_password'. If no custom password is selected, then the default of "coalescence" will be used instead.
Both the URL for resetting the admin's password and the new password itself are printed, so to login as admin, simply enter the new password.
