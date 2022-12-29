# check_nsxalb
scripts to monitor NSX Advanced Loadbalancer (AVI networks) cloud controller cluster and config parameters

## avicontrollercheck
Script avicontrollercheck.py takes ip address/user name/password of the Controller cluster and outputs 
- Cluster health
- cluster config parameters
- tenant configs including virtual services, pools, Service engine configs etc..

```
$ python avicontrollercheck.py -h
usage: avicontrollercheck.py [-h] -i IP -u USER -p PASSWD -o {health,cluster_configs,tenant_configs,se_group} [-n NAME]

NSX-ALB Cluster check Tool

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        NSX-ALB Controller VIP IP
  -u USER, --user USER  NSX-ALB Controller VIP User
  -p PASSWD, --passwd PASSWD
                        NSX-ALB Controller VIP Password
  -o {health,cluster_configs,tenant_configs,se_group}, --option {health,cluster_configs,tenant_configs,se_group}
                        Various configs checks
  -n NAME, --name NAME  Optional Name for check like --option se_group
```

## Checks for Nagios Plugin

### 1 - Nagios Plugin: cluster_health_check.py
Summary format of health check.

```
usage: cluster_health_check.py [-h] -i IP -u USER -p PASSWD

Script to check NSX-ALB cluster health

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        NSX-ALB controller VIP IP
  -u USER, --user USER  Controller admin user
  -p PASSWD, --passwd PASSWD
                        Controller admin password
```

SAMPLE Output
```
read -p "Enter Password: " -s PASSWD ;echo

./cluster_health_check.py -i nsx-alb.mylab.local -u admin -p "${PASSWD}"

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++Checking NSX-ALB Controller cluster+++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+Creating a session to NSX-ALB Controller nsx-alb.mylab.local

+++++++++Checking NSX-ALB cluster Status++++++++++
+Retrieving cluster health via API call https://nsx-alb.mylab.local/api/cluster/runtime
Current Cluster Status  : CLUSTER_UP_NO_HA
Cluster is up since     : 2022-11-25 10:48:01
+++++++++Checking cluster Member Status++++++++++
192.168.10.9 :   CLUSTER_LEADER  CLUSTER_ACTIVE  Up Since    2022-11-25 10:48:01

+++++++++Cluster is Unhealthy and the state is CLUSTER_UP_NO_HA ++++++++++
```


### 2 - Nagios Plugin: se_group_check.py

Search and check an SE Group **NAME** in all cloud and return its status.


```
usage: se_group_check.py [-h] -i IP -u USER -p PASSWD -n NAME [-d]

Script to check NSX-ALB cluster health
usage: se_group_check.py [-h] -i IP -u USER -p PASSWD -n NAME [-d]

Script to check NSX-ALB service engine group

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        NSX-ALB controller VIP IP
  -u USER, --user USER  Controller admin user
  -p PASSWD, --passwd PASSWD
                        Controller admin password
  -n NAME, --name NAME  SE Group Name
  -d, --debug           Debug Mode
```

SAMPLE Output-1
```
read -p "Enter Password: " -s PASSWD ;echo

./se_group_check.py -i nsx-alb.mylab.local -u admin -p ${PASSWORD} --name VCD-SE-GROUP-TEST

+++++++++Checking Service Engines in MY_NSXT_CLOUD/VCD-SE-GROUP-TEST++++++++++
nsx_avi__TEST-se-wthac : OK LICENSE_STATE_LICENSED OPER_UP Since 2022-12-29 11:48:09
nsx_avi__TEST-se-fnwdo : OK LICENSE_STATE_LICENSED OPER_UP Since 2022-12-29 11:48:35
+++++++++Overall Status of Service Engine Group MY_NSXT_CLOUD/VCD-SE-GROUP-TEST++++++++++
Service Engine Group Status : OK   HAVE_VIRTUAL_SERVICE
```

SAMPLE Output-2
```
read -p "Enter Password: " -s PASSWD ;echo

./se_group_check.py -i nsx-alb.mylab.local -u admin -p ${PASSWORD} --name VCD-SE-GROUP-TEST

+++++++++Overall Status of Service Engine Group MY_NSXT_CLOUD/VCD-SE-GROUP-TEST++++++++++
Service Engine Group Status : OK   NO_VIRTUAL_SERVICE
```

SAMPLE Output-3
```
read -p "Enter Password: " -s PASSWD ;echo

./se_group_check.py -i nsx-alb.mylab.local -u admin -p ${PASSWORD} --name VCD-SE-GROUP-TEST

+++++++++Overall Status of Service Engine Group MY_NSXT_CLOUD/VCD-SE-GROUP-TEST++++++++++
Service Engine Group Status : KO   NO_SE_IN_GROUP+UPGRADE_FSM_INIT+HAVE_VIRTUAL_SERVICE
```

