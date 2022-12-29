#!/usr/bin/env python
# Filename: se_group_check.py
# usage python se_group_check.py -i <controller vip ip> -u <admin user> -p <password> -n <se_group_name> [--debug]

__author__ = 'odraghi'

import requests
import json
import sys
import argparse
import datetime


def _debug(message):
    global debug_mode
    if debug_mode:
        print(f"+{message}")


def _create_session(avi_vip, avi_user, avi_passwd):

        _debug(f"Creating a session to NSX-ALB Controller {avi_vip}\n")
        avi_uri = f"https://{avi_vip}/login"
        try:
                requests.packages.urllib3.disable_warnings()
                login = requests.post(avi_uri, verify=False,
                                      data={'username': avi_user, 'password': avi_passwd})
                return login

        except Exception as api_excep:
            print("!!!!Exception Occurred while trying to create a session to NSX-ALB controlelr!!!")
            print(api_excep)


def _check_se_group(avic, avi_vip, group_name):
        is_healthy = False

        try:
                avi_uri = f"https://{avi_vip}/api/serviceenginegroup-inventory/?page_size=200&include=config,upgradestatus&include_name=true"

                if group_name:
                    avi_uri += f"&name={group_name}"
                
                resp = requests.get(avi_uri, verify=False, cookies=dict(sessionid= avic.cookies['sessionid']))
                
                results = json.loads(resp.text)['results']
                if not results:
                    print(f"+++++++++Overall Status of Service Engine Group {group_name}++++++++++")
                    print(f"Service Engine Group Status : KO   NOT_FOUND")
                    return is_healthy

                results_ok=0
                for result in results:
                    seg_state_err=[]
                    seg_info=[]

                    cloud=result['config']['cloud_ref'].split("#")[1]

                    _debug(f"+++++++++Checking Service Engine Group {cloud}/{group_name}++++++++++")
                    _debug(f"Upgrade state                     : {result['upgradestatus']['state']['state']}")
                    _debug(f"Service Engines Deprovision Delay : {result['config']['se_deprovision_delay']}")
                    _debug(f"Service Engines Min               : {result['config']['min_se']}")
                    _debug(f"Service Engines Current           : {len(result['serviceengines'])}")
                    _debug(f"Virtual Services Current          : {len(result['virtualservices'])}")
                    
                    if result['upgradestatus']['state']['state'] not in ('UPGRADE_FSM_COMPLETED'):
                        seg_info.append(result['upgradestatus']['state']['state'])


                    if result['virtualservices']:
                        seg_info.append("HAVE_VIRTUAL_SERVICE")
                        if result['serviceengines']:
                            print(f"+++++++++Checking Service Engines in {cloud}/{group_name}++++++++++")
                            count_se_ok=0
                            for se_long_href in result['serviceengines']:
                                se_href=se_long_href.split("#")[0]
                                se_href+="?join_subresources=runtime"
                                resp = requests.get(se_href, verify=False, cookies=dict(sessionid= avic.cookies['sessionid']))
                                service_engine = json.loads(resp.text)
                                se_state="KO"
                                if service_engine['enable_state'] in ('SE_STATE_ENABLED'):
                                    if ( service_engine['runtime']['oper_status']['state'] in ('OPER_UP') ) and (service_engine['license_state'] in ('LICENSE_STATE_LICENSED')):
                                        se_state="OK"
                                        count_se_ok+=1
                                else:
                                    se_state="DISABLED"
                                print(f"{service_engine['name']} : {se_state} {service_engine['license_state']} {service_engine['runtime']['oper_status']['state']} Since {datetime.datetime.fromtimestamp(service_engine['runtime']['oper_status']['last_changed_time']['secs'])}")
                            if count_se_ok < int(result['config']['min_se']):
                                seg_state_err.append("NOT_ENOUGH_OERATIONAL_SE_IN_GROUP")
                        else:
                            seg_state_err.append("NO_SE_IN_GROUP")
                    else:
                        seg_info.append("NO_VIRTUAL_SERVICE")

                    seg_state="KO"
                    if not seg_state_err:
                        seg_state="OK"
                        results_ok += 1
                    print(f"+++++++++Overall Status of Service Engine Group {cloud}/{group_name}++++++++++")
                    print(f"Service Engine Group Status : {seg_state}   {'+'.join(seg_state_err + seg_info )}")

                if results_ok == len(results):
                    is_healthy = True

                print()

                avic.close()


        except Exception as api_excep:
            print("!!!!Exception Occurred while getting configs from serviceenginegroup-inventory!!!")
            print(api_excep)


        return is_healthy


debug_mode=False

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Script to check NSX-ALB service engine group')
    parser.add_argument('-i','--ip', help='NSX-ALB controller VIP IP',required=True)
    parser.add_argument('-u','--user',help='Controller admin user', required=True)
    parser.add_argument('-p','--passwd',help='Controller admin password', required=True)
    parser.add_argument('-n', '--name', help="SE Group Name", required=True)
    parser.add_argument('-d', '--debug', help="Debug Mode",action='store_true', default=False, required=False)
    args = parser.parse_args()
    
    debug_mode=args.debug


    _debug("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    _debug("+++++++++Checking NSX-ALB Service Engine Group+++++++++++++")
    _debug("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    login_session = _create_session(args.ip, args.user, args.passwd)
    is_healthy=_check_se_group(login_session, args.ip, args.name)
    _debug(f"is_healthy: {is_healthy}")
    login_session.close()
