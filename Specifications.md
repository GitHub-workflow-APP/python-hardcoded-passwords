# Introduction

Below spec's are based on following thought process:

- 	This effort is largely driven by customer complains specially in PoVs. We plan to have functionality ready in production to move super quickly supporting a viable FN situation.
- 	This is also a duplicate effort since with python scanner -> saf migration we would get this functinality for free :). But, we recognize we can't wait for the migration limelight to support this. Thus, we have specc'ed this which will have a minimal effort, temparory fix which can cover a much bigger ground (max ROI). 
- 	This is going to be a bit of trial and error based approach balancing FP/FN.
- 	We also might need to be careful with the performance hit we might take since these checks would be per variable.
- 	We should try to not do anything more than saf... since we might land up not finding flaws we find now once we migrate to saf.


# Modeling	

The way I envision dividing this work is in broadly below 2 categories:

1. Variable assignments based 259s:

We would apply these checks for all variables which are hardcoded. Thus would be flagged only for variables. We would not be doing any checking of the context of the variable (for e.g. is it used in Django/flask/aws application) or if the variable is further used in the code. We broadly see 2 types of flaws here:
	
1a. **Exact match variable names:** We would define a list of exact matches and see how python scanner performance based on above listed criteria. We would add modify this list as required. Source of truth for this list will always be python scanner code. For e.g. We would flag variable named `password`, `passwd` etc. 

1b. **Fuzzy matching variable names:** This would be slightly more inclusive list than above approach, where we define some ligher performance regexp. For e.g. `(api|app|ssh).?key` where we are looking for just a single character. Again, this list will take maximum performance hit due to regexp checking for each hard coded variable used in entire project. We need to keep a close eye on these flaws.
	

2. Hardcoded passwords used in APIs (a.k.a sink based) based 259s:
	
	There are several APIs in python across different languages and frameworks where hardcoded secrets can be used such as connection strings, keyword arguments (password, secret_key etc). We will try to enlist such APIs and corresponding arguments to look for. While doing this, we should be careful we shouldn't be flagging twice, first time for above variable based heurtistic and 2nd time at the corresponding API. For e.g:

	```
	password = "some-not-to-be-hardcoded-value" # CWEID 259
	conn2 = psycopg2.connect(dbname="test", user="postgres", password=password) # FP CWEID 259 shouldn't be flagged
	```

	
	- JWT (ENG-24342)
		https://pyjwt.readthedocs.io/en/stable/usage.html

		`jwt.encode` contains a keyword argument `secret_key`, look for hardcoded value here.
	
	- Database API calls
		- **[mysql-connector](https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html)**
			
			Below 2 APIs can potentially have hardcoded passwords:

			1. mysql.connector.connect
			2. mysql.connector.connection

			Both the above apis will have a `password` keyword argument which should be checked if contains hardcoded passwords:

			```
				cnx = mysql.connector.connect(user='scott', password='password', # CWEID 259
                              host='127.0.0.1',
                              database='employees')
			```

			Also, 

			```
			passcode = "passw0?d" # CWEID 259
			cnx3 = connection.MySQLConnection(user='scott', password=passcode, 
                                 host='127.0.0.1',
                                 database='employees')

			```
	
		- **[postgres-connector](https://www.psycopg.org/docs/)**
				`psycopg2.connect` will have a `password` keyword argument. Look for hardcoded values in this api.
			
		- **django db:** ToDo
		- **flask db:** ToDo

	- Cloud Services	
		- [boto3.session](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session):
			`boto3.session.Session`, keyword arguments to look for `aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`
			`boto3.session.Session.client`, keyword arguments to look for `aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`
			`boto3.session.Session.resource`, keyword arguments to look for `aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`

		
	- Crypto APIs

# Testcases:

https://gitlab.laputa.veracode.io/research-roadmap/python-hardcoded-passwords/-/tree/main/research-testcases

# Accepted False Negative Scenerios:

1. We don't scan with-in comments:

```
#pwd = "super-secret-password"  # FN We don't scan comments
```

2. Variables which might look like high potential of holding sensitive information, we wont be parsing parts of it to detect for hidden secrets. For e.g.

```
url = "http://somehost.com/XDmkwdlp/iuuibcdjquihcSD=" # FN, even if it could be potential tokens
```

3. Without knowing where a variable is being used, even if it contains hints that something sensitive could be potentially present we won't flag it. 

```
from unsupported.package import something-unsupported
...
conn_str = ".....AccountKey=SOME-SUPER-SECRET-KEY" # CWEDID FN 259, since we don't understand the usage of this string 
client = something-unsupport.connect(conn_str) 

```

# Potential Future Enhancements

- Hardcoded in if statements

```
if username == 'admin':
	...
```

