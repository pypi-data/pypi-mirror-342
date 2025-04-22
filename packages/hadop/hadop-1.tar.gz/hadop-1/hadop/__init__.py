def one():
    print('''
cut -d: -f1 /etc/passwd

# remove hadoop user
sudo deluser hduser

# ps aux | grep 
sudo killall -TERM -u hduser

## remove hadoop group
sudo deluser --group hadoop

# check presence of hadoop
# go to location  /usr/local/
# if you see a hadoop folder then hadoop installation was attempted and needs to be  removed before fresh installation

# remove hadoop
sudo rm -r -f /usr/local/hadoop/

==========================================

Step 1 — Installing Java
Step 2 — Installing Hadoop
Step 3 — Configuring Hadoop
Step 4 — Running Hadoop
===========================================================================

Step 1 — Installing Java
To get started, we’ll update our package list:
sudo apt update
 
Next, we’ll install OpenJDK, the default Java Development Kit on Ubuntu 18.04:
sudo apt install default-jdk

check folder for java installation at location - 
java path -/usr/lib/jvm/java-11-openjdk-amd64
Once the installation is complete, let’s check the version.
java -version
This output verifies that OpenJDK has been successfully installed.


===========================================================================
#Add newuser to new usergroup
#group-hadoop, #user - hduser
sudo addgroup hadoop
sudo adduser --ingroup hadoop hduser

#add new user to listed groups
sudo usermod -aG sudo hduser

#change to new user
su hduser
#The prompt shoud look like this - hduser@ubuntu:/
===========================================================================
#Create a ssh keygen for the user.
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

# Disable IPv6.
sudo nano /etc/sysctl.conf

#add the following lines to the end of the file
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
===========================================================================
Step 2 — Downloading & Installing Hadoop
===========================================================================
#Extract Hadoop and move to group hadoop
cd /usr/local

sudo tar xvf /home/udit/Downloads/hadoop-3.2.3.tar.gz 
sudo mv hadoop-3.2.3 hadoop
sudo chown -R hduser: hadoop hadoop
===========================================================================
#Now open $HOME/.bashrc 
sudo nano $HOME/.bashrc

#add the following lines
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin

#Save file - Ctrl + s
#Close file - Ctrl + x

#Run the following command to make changes through the .bashrc file.
source ~/.bashrc

#Check version of java and hadoop
Command: java -version
Command: hadoop version
===========================================================================
===========================================================================
#Create a tmp folder in /app/hadoop/tmp and change the owner to hduser.
cd /usr/local
sudo mkdir -p /app/hadoop/tmp
sudo chown hduser:hadoop /app/hadoop/tmp/
===========================================================================
Step 3 — Configuring Hadoop
# Hadoop requires that you set the path to Java, either as an environment variable or in the Hadoop configuration file.hadoop-env.sh
cd /usr/local/hadoop/etc/hadoop/

#To Configure Hadoop’s Java Home, begin by opening hadoop-env.sh
sudo nano hadoop-env.sh

#Add the following line at the end of .sh file
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# save & close


#Make the changes in core-site.xml file
cd /usr/local/hadoop/etc/hadoop
sudo nano core-site.xml

#Add the following lines
<property>
	<name>hadoop.tmp.dir</name>
	<value>/app/hadoop/tmp</value>
	<description>A base for other temporarary directories</description>
</property>

<property>
	<name>fs.default.name</name>
	<value>hdfs://localhost:54310</value>
	<description>The name of the default file system.</description>
</property>

# save & Close
===========================================================================
#Make the changes in mapred-site.xml
sudo nano mapred-site.xml

#Add the following lines
<property>
	<name>mapred.job.tracker</name>
	<value>localhost:54311</value>
	<description>The host and port that the MapReduce job tracker runs
		at. If "local", then jobs are run in-process as a single map
		and reduce task.
	</description>
</property>
# save & Close
===========================================================================
#Make the changes in hdfs-site.xml
===========================================================================
sudo nano hdfs-site.xml

#Add the following lines
<property>
            <name>dfs.namenode.name.dir</name>
            <value>/app/hadoop/tmp/dfsdata/namenode</value>
    </property>

    <property>
            <name>dfs.datanode.data.dir</name>
            <value>/app/hadoop/tmp/dfsdata/datanode</value>
    </property>

<property>
	<name>dfs.replication</name>
	<value>1</value>
	<description>Default block replication.
		     The actual number of replications can be specified when the file is 		     created. The default is used if replication is not specified in  			     create time.
	</description>
	
</property>

# save & Close
===========================================================================
#format namenode 
hdfs namenode -format
hdfs datanode -format
===========================================================================
# Step 4 - Running Hadoop
su hduser
          
cd /usr/local/hadoop/sbin

# To start hadoop, we need to start localhost
ssh localhost

# If connection is refused, it will result in error - run only if error & then run previous command
sudo apt-get install ssh

# Start all the hadoop services
/usr/local/hadoop/sbin/start-all.sh

# Check if that all hadoop services are running (6 services should appear)
jps

#Access localhost:9870 to get nanmenode status, open browser and type
http://localhost:9870

#Stop all the hadoop services.
/usr/local/hadoop/sbin/stop-all.sh
''')
def two():
    print('''
          
    1) Login to Hadoop user: hduser:udit@123
su hduser
          
cd /usr/local/hadoop/sbin


    2) Start hadoop services & verify
ssh localhost
/usr/local/hadoop/sbin/start-all.sh
Jps

    3) Check if hadoop is installed via terminal
hadoop version

    4) Check if hadoop is installed via browser
http://localhost:9870

    5) Create a folder named “sds_your_roll_no” in /usr/local/ ex. Sds_a20
cd /usr/local
sudo mkdir -p /usr/local/sds_a016
ls

    6) Assign full privileges to sds_ your_roll_no
sudo chmod -R 777 /usr/local/sds_a016
ls

    7) Create a file named nmimstext.txt in /usr/local/sds_your_roll_no with the following text:
cd /usr/local/sds_a016
sudo nano nmimstext.txt
ls
cat nmimstext.txt

    8) Create a folder named “SDS” in HDFS root folder
cd /usr/local/hadoop/bin/
hdfs dfs -mkdir /SDS
hdfs dfs -ls /

    9) Move the file nmimstext.txt to SDS folder in HDFS & verify if its moved
hdfs dfs -copyFromLocal /usr/local/sds_a016/nmimstext.txt /SDS
hdfs dfs -ls /SDS 

    10) Read the contents of file nmimstext.txt from the HDFS location
cd /home/udit
hdfs dfs -cat /SDS/nmimstext.txt
''')    
    
def three():
    print('''
    1) Login to Hadoop user: hduser:udit@123
su hduser

cd /usr/local/hadoop/sbin
          
    2) Start hadoop services & verify
ssh localhost
/usr/local/hadoop/sbin/start-all.sh
Jps

    3) Check if hadoop is installed via terminal
hadoop version

    4) Check if hadoop is installed via browser
http://localhost:9870

    5) Create a folder named “sds_your_roll_no” in /usr/local/ ex. Sds_a20
cd /usr/local
sudo mkdir -p /usr/local/sds_a016
ls

    6) Assign full privileges to sds_ your_roll_no
sudo chmod -R 777 /usr/local/sds_a016
ls

    7) Create a file named nmimstext.txt in /usr/local/sds_your_roll_no with the following text:
cd /usr/local/sds_a016
sudo nano nmimstext.txt
ls
cat nmimstext.txt

    8) Create a folder named “SDS” in HDFS root folder
cd /usr/local/hadoop/bin/
hdfs dfs -mkdir /SDS
hdfs dfs -ls /

    9) Move the file nmimstext.txt to SDS folder in HDFS & verify if its moved
hdfs dfs -copyFromLocal /usr/local/sds_a016/nmimstext.txt /SDS
hdfs dfs -ls /SDS 

    10) Read the contents of file nmimstext.txt from the HDFS location
cd /home/udit
hdfs dfs -cat /SDS/nmimstext.txt
''')    
    
      
def four():
    print('''
Start the hadoop and verify all services are started
/usr/local/hadoop/sbin/start-all.sh


          Download the Pig Package file:
wget https://downloads.apache.org/pig/pig-0.17.0/pig-0.17.0.tar.gz

          Navigate to /usr/local/

sudo tar xzvf /home/hduser/Downloads/pig-0.17.0.tar.gz
sudo mv pig-0.17.0-src/pig


          Add the Pig environment variables in bashrc and      check the pig version to verify the installation.
sudo nano ~/.bashrc     

          # Add the following lines
export PIG_HOME=/usr/local/pig	
export PATH=$PATH:$PIG_HOME/bin
export PIG_CLASSPATH=$HADOOP_HOME/conf

pig –-version

 
          Create a database file.
sudo nano products.txt

          Enter some text like (without spaces)
1,phone,45,mumbai,2023
2,laptop,44,pune,2022


          Run the pig in Local mode and load the products file
pig -x local
product = LOAD 'products.txt' USING PigStorage(',');
dump product;


          Running in HDFS mode
          First we need to move products.txt to HDFS

hdfs dfs -put /usr/local/products.txt/
pig
product = LOAD 'hdfs://localhost:54310/products.txt' USING PigStorage(',');
dump product;


          Use of DISTINCT operator in PIG. Assume appropriate data in text files.
sudo nano m3.txt


          Use of FILTER operator in PIG
m3 = LOAD 'm3.txt' USING PigStorage(',') as (a1:int,a2:int,a3:int);
result_f = filter m3 by a3==6;
dump result_f

          Use of ORDERBY operator in PIG
result_ob = ORDER m3 BY a1 ASC;
dump result_ob;


          Use of UNION operator in PIG
Sudo nano m1.txt

''')    
          

def five():
    print('''
/usr/local/hadoop/sbin/start-all.sh

    Navigate to /usr/local/
sudo tar xvzf /home/hduser/Downloads/apache-hive-3.1.2-bin.tar.gz
sudo mv apache-hive-3.1.2-bin/ hive
sudo chmod 777 hive
    Add the HIVE_HOME path in the bashrc file.
sudo nano ~/.bashrc
    #add following lines 
export HIVE_HOME=/usr/local/hive
export PATH=$PATH:$HIVE_HOME/bin

source ~/.bashrc

Change the directory to /usr/local/hive/bin 
     and add the following lines in hive-config.sh
cd /usr/local/hive/bin     
sudo nano hive-config.sh
export HADOOP_HOME=/usr/local/hadoop

    
    Hive is installed now, but  we need to first create some directories in HDFS for Hive to store its data
hdfs dfs -mkdir /tmp
hdfs dfs -chmod g+w /tmp
hdfs dfs -chmod o+w /tmp
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -chmod g+w /user/hive/warehouse
hdfs dfs -chmod 777 /tmp
hdfs dfs -chown -R hduser:supergroup /user/hive/warehouse
hdfs dfs -chmod -R 777 /user/hive/warehouse
hdfs dfs -ls /

    Initialze the database schema
cd /$HIVE_HOME/bin
sudo ./schematool -initSchema -dbType derby
    There is compatibility error between Hadoop and Hive guava versions.
    To fix the NoSuchMethodError, Locate the guava jar file in the Hive lib directory
    Remove the guava jar file from /hive/lib
sudo rm lib/guava-19.0.jar
    # Copy the guava jar from hadoop lib to hive lib directory
sudo cp $HADOOP_HOME/share/hadoop/common/lib/guava-27.0-jre.jar /usr/local/hive/lib/
    # Once copied, Use the schematool command once again to initiate the Derby database.
cd /$HIVE_HOME/bin
sudo ./schematool  -initSchema -dbType derby
    # Note for Error: FUNCTION 'NUCLEUS_ASCII' - 
sudo rm -rf metastore_db
    Start HIVE:
cd /usr/local/hive/bin
sudo ./hive
	
    Create a database and show
create database company

    Create Employee table
create table employees (id int, name string, country string, department string, salary int) row format delimited fields terminated by ' ';

    Load the data into a table from a file
sudo nano employees.txt
    Enter few rows without spaces

load data local inpath "./employees.txt" into table employees;
    Reading the Table Data
select * from employees;

''')    
def six():
    print('''

cd /usr/local/hive/bin
sudo ./hive
create database show_bucket;
show databases;
use show_bucket;

create table emp_demo (id int, name string, salary int)
row format delimited
fields terminated by ',';

show tables;
quit;

sudo nano emp_details.txt
1,Example1,95000
2,Example2,85000
3,Example3,90000
4,Example4,80000
5,Example5,75000
         
ls
sudo ./hive
use show_bucket
load data local inpath 'emp_details.txt' into table emp_demo;

DESCRIBE emp_demo;
set hive.enforce.bucketing = true;
create table emp_bucket (id int, name string, salary int)
row format delimited
fields terminated by ',';

#go to localhost:9870
/usr/hive/warehouse/show_bucket.db
          
insert overwrite table emp_bucket select * from emp_demo; 
hdfs dfs -ls /user/hive/warehouse/show_bucket.db/emp_bucket
 
/usr/hive/warehouse/show_bucket.db/emp_bucket

DROP DATABASE IF EXISTS student CASCADE; 
DROP DATABASE IF EXISTS show_bucket CASCADE; 
DROP DATABASE IF EXISTS company CASCADE; 
DROP DATABASE IF EXISTS school CASCADE; 

show databases;
hdfs -dfs -rm -r /SDS

cd /usr/local
sudo rm -rf sds_a016


''')

def sevena():
    print('''
1. The .collect() Action
collect_rdd = sc.parallelize([1,2,3,4,5])
print(collect_rdd.collect())
          
2. The .count() Action
count_rdd = sc.parallelize([1,2,3,4,5,5,6,7,8,9])
print(count_rdd. count())
          
3. The .first() Action
first_rdd = sc.parallelize([1,2,3,4,5,6,7,8,9,10])
print(first_rdd.first())
          
4. The .take() Action
take_rdd = sc.parallelize([1,2,3,4,5])
print(take_rdd.take(3))
          
5. The .reduce() Action
reduce_rdd = sc.parallelize([1,3,4,6])
print(reduce_rdd.reduce(lambda x, y : x + y) )
          
6. The .saveAsTextFile() Action
save_rdd = sc.parallelize([1,2,3,4,5,6])
save_rdd. saveAsTextFile('file.txt')
          
#Transformations in PySpark RDDs

1. The .map() Transformation
my_rdd = sc.parallelize([1,2,3,4])
print(my_rdd.map(lambda x: x+ 10).collect())
          
2. The .filter() Transformation
filter_rdd = sc.parallelize([2, 3, 4, 5, 6, 7])
print(filter_rdd.filter(lambda x: x%2 == 0).collect())
          
filter_rdd_2 = sc.parallelize(['Rahul', 'Swati', 'Rohan', 'Shreya', 'Priya' ])
print(filter_rdd_2.filter(lambda x: x.startswith('R')).collect())
          
3. The .union() Transformation
union_inp = sc.parallelize([2,4,5,6,7,8,9])
union_rdd_1 = union_inp.filter(lambda x: x % 2 == 0)
union_rdd_2 = union_inp.filter(lambda x: x % 3 == 0)
print(union_rdd_1.union(union_rdd_2).collect())
          
4. The .flatMap() Transformation
flatmap_rdd = sc.parallelize(["Hey there", "This is PySpark RDD Transformations"])
(flatmap_rdd.flatMap(lambda x: x.split("")).collect())
          
#PySpark Pair RDD Operations
marks = [('Rahul', 88), ('Swati', 92), ('Shreya', 83), ('Abhay', 93), ('Rohan',78)]
sc.parallelize(marks).collect()
print(marks_rdd.reduceByKey(lambda x, y: x + y).collect())
''')

def sevenb():
    print('''
Step 1: Update System Packages
First, update and upgrade the system packages:
sudo apt update && sudo apt upgrade -y
________________________________________
Step 2: Install Java (OpenJDK 11)
Apache Spark requires Java. Install OpenJDK 11:
sudo apt install openjdk-11-jdk -y
Verify installation:
java -version
 
Expected output:
openjdk version "17.0.x" ...
________________________________________
Step 3: Install Scala
Spark requires Scala for execution:
sudo apt install scala -y
 
Verify installation:
scala -version
 
________________________________________
Step 4: Download and Install Apache Spark
Download the latest Apache Spark (3.x) release:
cd /opt	 
 
 
sudo wget https://downloads.apache.org/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz
 
Extract the archive:
sudo tar -xvzf spark-3.5.5-bin-hadoop3.tgz
 
Rename the folder:
sudo mv spark-3.5.5-bin-hadoop3 spark
 
________________________________________
Step 5: Set Up Environment Variables
Edit the. bashrc file:
nano ~/.bashrc
 
Add the following lines at the end:
export SPARK_HOME=/opt/spark
export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
export PYSPARK_PYTHON=/usr/bin/python3
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
Save and exit (Ctrl+S & Ctrl+X).
 
Apply the changes:
source ~/.bashrc
 
________________________________________
Step 6: Start Spark
Start Spark Master and Worker
start-master.sh
 
Find the Spark Master URL in the output (e.g., spark://yourhostname:7077).
________________________________________
🔍 Next Steps: Verify Spark Master UI
You can now access the Spark Master Web UI to confirm everything is working:
📍 Open your browser and go to:
http://localhost:9870
 
You should see a dashboard showing:
•	Spark version
•	Master URL (e.g., spark://ubuntu:7077)
•	Worker nodes (currently 0 if none are started yet)

________________________________________
Now, start a worker:
### 	start-worker.sh spark://yourhostname:7077 
start-worker.sh spark://ubuntu:7077
 
To check if Spark is running, open a browser and go to:
➡ http://localhost:9870
 
________________________________________
Step 7: Start Spark Shell
Start the interactive Spark shell:
spark-shell


Verify the installation by running:
sc.appName
 

Step 1: Launch PySpark Shell
From your terminal (bash, like this: udit@ubuntu:/opt$), 

Pyspark
 
If it's correctly installed, your prompt will change to:
>>> 	#######This is the PySpark (Python) shell.
 
Step 2: Create an RDD
Create an RDD from a Python list:
rdd = sc.parallelize([1, 2, 3, 4, 5])
print(rdd.collect())				  # Output: [1, 2, 3, 4, 5]
 
Step 3: Apply Transformations
Apply map() transformation to square each number:
squared_rdd = rdd.map(lambda x: x ** 2)
print(squared_rdd.collect())  # Output: [1, 4, 9, 16, 25]
 
Your PySpark command executed successfully, However, you are seeing a SocketTimeoutException, which is a common issue in Spark when running in local mode. It does not affect the correctness of your computations, but it indicates a network communication timeout in Spark’s internal processes.

Apply filter() transformation to keep even numbers:
even_rdd = rdd.filter(lambda x: x % 2 == 0)
print(even_rdd.collect())  # Output: [2, 4]
 
Step 4: Perform Actions
Use the reduce() action to sum all elements:
sum_rdd = rdd.reduce(lambda a, b: a + b)
print(sum_rdd)


''')
    
def eight():
    print('''
# Step 1:  Install mongodb by executing the installation file "mongodb-windows-x86_64-4.4.6-signed"
 # Click next, next and finish the installation

# Step2: Launch MongoDB
# Navigate to the following location: "C:\Program Files\MongoDB\Server\4.4\bin"

#Start mongo daemon - 
mongod

#Start mongo service - 
mongosh

# Show list of db
show dbs 
 
# Show current db
db 

# Create/switch to a db - use dbname
use udit
 
# Display existing collections
show collections;
 
# Create collection - db.collectionname
db.subjects
 

# Insert into collection
db.subjects.insertOne({"name":"bda"})
db.subjects.insertOne({"name":"mn"})
db.subjects.insertOne({"name":"ip"})
db.subjects.insertOne({"name":"msa"})
show collections;
 

# Display all records in collection
db.subjects.find();
 

# Display specific record in colleciton
db.subjects.find({"name": "bda"});
 

# Using MongoDB With Python and PyMongo
# Install python 3.7.4
# Launch IDLE 3.7

# Installing PyMongo (in cmd)
# MongoDB provides an official Python driver called PyMongo.
python -m pip install pymongo
 

# Start a Python interactive session and run the following import:
import pymongo

#Working With Databases, Collections
# Program 1: Creating a Database
from pymongo import MongoClient              	      //import MongoClient from pymongo. 

# Create a client object to communicate with running MongoDB instance
myclient = MongoClient()                                    
myclient				        					//test client

# To provide a custom host and port when you need to provide a host and port that differ from MongoDB’s default
myclient = MongoClient(host="localhost", port=27017)

# Check db list
print(myclient.list_database_names())

# Define which database you want to use
db = myclient["udit"]

# Progam 2: Creating a Collection
import pymongo
myclient = MongoClient(host="localhost", port=27017)
db = myclient.mlib 
col=db.subjects1                                                                 	 
dict = {"name":"ds", "sem":"1"}	           			 
x=col.insert_one(dict)                                               		 

print(client1.list_database_names())

''')

def nine():
    print('''
Step 1: Install Java (Prerequisite)
Apache Storm requires Java. Install OpenJDK if it’s not already installed:
	sudo apt update
	
 

	sudo apt install -y openjdk-17-jdk

Verify the installation:
java -version	
 
 
________________________________________
🦓 3. Install ZooKeeper
Apache Storm relies on Apache ZooKeeper for coordination.
	sudo apt install -y zookeeperd

 

Start the ZooKeeper service:

	sudo systemctl start zookeeper
	sudo systemctl enable zookeeper
 
  
	sudo systemctl status zookeeper

 

Verify that ZooKeeper is running:
	echo "ruok" | nc localhost 2181

 

If it returns imok, ZooKeeper is running correctly.

________________________________________
🌩️ 4. Download and Install Apache Storm
Download the latest Apache Storm release:
cd /opt

sudo wget https://downloads.apache.org/storm/apache-storm-2.8.0/apache-storm-2.8.0.tar.gz.sha512

 
Extract the archive:
sudo tar -xvzf apache-storm-2.8.0.tar.gz


 

sudo mv apache-storm-2.8.0 storm
Set permissions:
		sudo chown -R $USER:$USER /opt/storm

 
________________________________________
🔧 5. Configure Apache Storm
Edit the storm.yaml configuration file:
	nano /opt/storm/conf/storm.yaml
 

Add or update the following lines:
	storm.zookeeper.servers:
	    - "localhost"

	nimbus.seeds: ["localhost"]
	
	supervisor.slots.ports:
    - 6700
    - 6701
    - 6702
    - 6703
ui.port: 8080

Save and exit (Ctrl + X, then Ctrl + S).



 
Create the local directory:
sudo mkdir /opt/storm/tmp
 
________________________________________
🚀 6. Start Apache Storm Services
In separate terminal tabs or with tmux/screen, run the following components:
Nimbus (Master node):
cd /opt/storm
bin/storm nimbus
Supervisor (Worker node):
cd /opt/storm
bin/storm supervisor
Storm UI (Web interface):
cd /opt/storm
bin/storm ui
Now, visit: http://localhost:8080 to view the Storm UI.
________________________________________
🧪 7. Submit a Sample Topology
Storm comes with example topologies.
cd /opt/storm
bin/storm jar examples/storm-starter/storm-starter-topologies-*.jar org.apache.storm.starter.ExclamationTopology exclamation-topology
This will submit a sample topology to your cluster.
________________________________________
To submit a sample topology in Apache Storm, follow these simple steps. This will help you test that your Storm setup is working properly.
________________________________________
✅ Step 3: Run the Sample Topology Command

bin/storm jar examples/storm-starter/storm-starter-topologies-*.jar org.apache.storm.starter.ExclamationTopology exclamation-topology
________________________________________
✅ After Submission
1.	Check Logs to confirm it's running properly.
2.	Visit the Storm UI (usually on port 8080):
3.	http://<your-nimbus-ip>:8080
Look for your exclamation-topology in the list.
________________________________________
💡 Optional: Kill the Topology Later
If you want to stop it:
bin/storm kill exclamation-topology

''')
    
def ten():
    print('''
1. Install Apache Solr
Install Java
Check if Java is installed:
java -version
 
If Java is not installed, install OpenJDK:
sudo apt update
sudo apt install openjdk-17-jdk -y

Verify Java installation:
java -version

Download Apache Solr
Go to Apache Solr's official website and get the latest stable version. Or download via wget:
wget https://downloads.apache.org/lucene/solr/9.5.0/solr-9.5.0.tgz
OR
wget https://archive.apache.org/dist/solr/solr/9.4.1/solr-9.4.1.tgz
(OR Change 9.5.0 to the latest version available.)

Verify the File Integrity
Check the file size:
			ls -lh solr-9.4.1.tgz
 
It should match the expected size (~268MB).
Extract and Install
tar xzf solr-9.5.0.tgz
cd solr-9.5.0

OR
tar xzf solr-9.4.1.tgz
cd solr-9.4.1

To install Solr as a system service:
sudo bash bin/install_solr_service.sh ~/solr-9.5.0.tgz
OR
sudo bash bin/install_solr_service.sh ~/solr-9.4.1.tgz


________________________________________
2. Run Apache Solr
After installation, start Solr with:
sudo systemctl start solr
To check if it's running:
sudo systemctl status solr

To stop Solr:
sudo systemctl stop solr

To restart Solr:
sudo systemctl restart solr
To verify Solr is running, open your browser and visit:
		http://localhost:8983/solr

 

This opens the Solr Admin UI.
________________________________________
3. Configure Apache Solr
Create a Collection

		sudo su - solr
 
A collection is equivalent to a database in SQL.
/opt/solr/bin/solr create -c mycollection -n _default
Replace mycollection with your preferred name.
/opt/solr/bin/solr create -c mydreams -n _default
 

🔧 1. Change Solr Configuration
Edit Core Config Files
Solr stores configurations in solrconfig.xml and schema.xml inside:
/var/solr/data/mydreams/conf/
 

Here’s a concise breakdown of how to change Solr configuration, enable authentication, index and search data, and monitor logs.
________________________________________
1.	Common Settings (Global config)
File: /etc/default/solr.in.sh
 
•	Change Port
SOLR_PORT=8984
•	Set Memory
SOLR_HEAP="2g"
________________________________________
🔐 2. Enable Basic Authentication
Edit /etc/default/solr.in.sh and add:
SOLR_AUTH_TYPE="basic"
SOLR_AUTHENTICATION_OPTS="-Dbasicauth=admin:admin123"
Replace admin:admin123 with your preferred username and password.

 
Restart Solr to Apply Changes
sudo systemctl restart solr
________________________________________
📥 3. Indexing Data
Add a Sample Document
curl -X POST -H "Content-Type: application/json" --data '
{
  "id": "1",
  "name": "Sample Document"
}' http://localhost:8983/solr/ mydreams /update?commit=true
________________________________________
🔍 4. Searching Data
From Browser
http://localhost:8983/solr/ mydreams /select?q=*
Using curl
curl "http://localhost:8983/solr/mydreams/select?q=*"
________________________________________
📈 5. Monitoring Logs
Tail Live Logs
tail -f /var/solr/logs/solr.log
You can also check service status:
sudo systemctl status solr


''')

def help():
    print('''
one() = Install, configure and run Hadoop and HDFS 
two() = File Management tasks in Hadoop File System 
three() = Implement word count program using MapReduce 
four() = nstall, configure and run Pig. Execute Pig Latin scripts to sort, group, join, project and filter data
five() = Install, configure and run Hive
six() = Implement Bucketing using Hive
sevena() = RDDS on Spark
sevenb() = Install, configure and run Apache Spark.
eight() = Install MongoDB and manipulate it using Python
nine() = Install, configure and run Apache Strom 
ten() = Install, configure and run Apache Solr 
''')