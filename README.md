# check_nsxalb
scripts to monitor NSX Advanced Loadbalancer (AVI networks) cloud controller cluster and config parameters

There are 2 scripts in this repo.

1) avicontrollercheck.py takes ip address/user name/password of the Controller cluster and outputs 
- Cluster health
- cluster config parameters
- tenant configs including virtual services, pools, Service engine configs etc..

```
$ python avicontrollercheck.py -h
usage: avicontrollercheck.py [-h] -i <IP> -u <USER> -p <PASSWD> -o <OPTION>
                             OPTION: health, cluster_configs, tenant_configs

AVI Cluster check Tool

optional arguments:
  -h, --help            show this help message and exit
  -i <IP>, --ip <IP>        AVI Controller VIP IP
  -u <USER>, --user <USER>  AVI Controller VIP User
  -p <PASSWD>, --passwd <PASSWD>
                        AVI Controller VIP Password
  -o <OPTION>, --option <OPTION>
  
  OPTION : health, cluster_configs, tenant_configs
                        Various configs checks
```

2) cluster_health_check.py
Summary format of health check. It can be used as a Nagios plugin.

