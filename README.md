Udetect
=======
A tool to monitor changes to your files, directories.

INSTALL
=======  
1. Installl Python 2.7 or higher.
2. Install Pip (recommend) or Easy Install (package manager for Python).  
	+ For Ubuntu/Debian
> sudo apt-get install python-pip

	For Fedora/Centos
> sudo yum -y install python-pip

	For Windows
> http://docs.python-guide.org/en/latest/starting/install/win/

3. Install Requirements
	+ Run command: 
>pip install -r requirements.txt

4. Run and Enjoy it!  

HOW TO USE
==========
1. Create Project to monitor a folder
>python udetect.py create projectname /path/project/  

2. Configuration  
udetect.conf  
>	[main_config]  
>	email = unstester@gmail.com  
>	smtp_pass = noP@ssW0rd  
>	smtp_port = 587  
>	smtp_server = smtp.gmail.com  
>	email_default = vietnguyen@uns.vn // if project 's email is default, Udetect will use this field to replace  
>
>	[atom]
>	enable = 1 //enable = 1, disable = 0  
>	white_ext = * // manage extensions exclusions. Ex: .txt .tmp  
>	white_dir = * // manage folders, files exclusions. Ex: /home/tester/test/logs/ /home/tester/test/cache/  
>	email = default // set default to use email_default 's value  
>	type = fast //fast, full

3. Run manual (or use Crontab on Linux)
>python udetect.py start  


SUPPORT
=======

Homepage: [http://uns.vn  ](link)  
Q&A: [http://uns.vn/qaa/](link)  
Email: vietnguyen@uns.vn
