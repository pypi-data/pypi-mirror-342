from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
collection = db["testcollection"]

# # Create
collection.insert_one({"name": "Alice", "age": 25})

# # Read
print(collection.find_one({"name": "Alice"}))

# Update
collection.update_one({"name": "Alice"}, {"$set": {"age": 26}})

# Delete
collection.delete_one({"name": "Alice"})

print(client.list_database_names())



'''

#!/bin/bash

# === Setup SSH ===
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

# === Update System ===
sudo apt update && sudo apt upgrade -y

# === Install Java ===
sudo apt install -y openjdk-11-jdk

# === Verify Java ===
java -version

# === Download Hadoop ===
cd /usr/local
sudo wget https://archive.apache.org/dist/hadoop/common/hadoop-3.2.3/hadoop-3.2.3.tar.gz

# === Extract Hadoop ===
sudo tar -xzf hadoop-3.2.3.tar.gz
sudo mv hadoop-3.2.3 hadoop
sudo rm hadoop-3.2.3.tar.gz

# === Set Hadoop Environment Variables ===
echo "
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export PATH=\$PATH:\$HADOOP_HOME/bin
export HADOOP_HDFS_HOME=$HADOOP_HOME
" | sudo tee -a ~/.bashrc

# Apply immediately
source ~/.bashrc

# === Configure Hadoop Core-Site ===
sudo tee /usr/local/hadoop/etc/hadoop/core-site.xml > /dev/null <<EOF
<configuration>
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
</configuration>
EOF

# === Configure HDFS Site ===
sudo tee /usr/local/hadoop/etc/hadoop/hdfs-site.xml > /dev/null <<EOF
<configuration>
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
The actual number of replications can be specified when the file is
created. The default is used if replication is not specified in
create time.
</description>
</property>
</configuration>
EOF

# === Configure MapReduce Site ===
sudo tee /usr/local/hadoop/etc/hadoop/mapred-site.xml > /dev/null <<EOF
<configuration>
<property>
<name>mapred.job.tracker</name>
<value>localhost:54311</value>
<description>The host and port that the MapReduce job tracker runs
at. If "local", then jobs are run in-process as a single map
and reduce task.
</description>
</property>
</configuration>
EOF

# === Update JAVA_HOME in hadoop-env.sh ===
echo "
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
" | sudo tee -a /usr/local/hadoop/etc/hadoop/hadoop-env.sh

# === Create Hadoop NameNode and DataNode Directories ===
sudo mkdir -p /app/hadoop/tmp
sudo chown -R $USER:$USER /app/hadoop/tmp

# === Format HDFS Namenode ===
hdfs namenode -format
hdfs datanode -format

# === Start localhost ===
ssh localhost

# === Start HDFS & YARN ===
/usr/local/hadoop/sbin/start-all.sh

# === Display Running Hadoop Daemons ===
jps


'''


