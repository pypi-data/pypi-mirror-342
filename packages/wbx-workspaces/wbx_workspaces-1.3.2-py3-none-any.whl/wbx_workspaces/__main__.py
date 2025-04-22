
import os
import json
import logging
import re      
import datetime
from datetime import timezone
import importlib.metadata
import sys
# from dotenv import load_dotenv, find_dotenv
from pprint import pprint
import click

import wbx_workspaces.wbx_utils as wbx_utils  
import wbx_workspaces.wbx_dataframe as wbxdf
import wbx_workspaces.wbx as wbx

ut=wbx_utils.UtilsTrc()
wbxr=wbx.WbxRequest()

# import variables in .env 
# load_dotenv(os.getcwd() + "/.env")

WBX_SCOPES = "spark-admin:workspaces_read spark-admin:devices_read spark-admin:workspace_metrics_read"

__version__ = my_name = "N/A"
try:
    __version__ = importlib.metadata.version(__package__)
    my_name = __package__
except:
    print("Local run")

logging.basicConfig()

###################
### Workspaces ### 
###################

@click.command()
@click.option('-c', '--csvfile', help='Save results to CSV file.')
@click.option('-r', '--rawdata', is_flag=True, help='Show json raw data')
def locations(csvfile, rawdata):
    """ List locations IDs."""
    locDF=wbxdf.locationsDF()
    locDF.print(csvfile)        
    if (rawdata):
        pprint(locDF.jsonList)


@click.command()
@click.option('-l', '--location_id', help='Restrict list to location Id')
@click.option('-c', '--csvfile', help='Save results to CSV file.')
@click.option('-r', '--rawdata', is_flag=True, help='Show json raw data')
def workspaces(csvfile, rawdata, location_id):
    """ List workspaces in given location. """
    workspacesDF=wbxdf.workspacesDF(location_id)
    workspacesDF.print(csvfile)        
    if (rawdata):
        pprint(workspacesDF.jsonList)


@click.command()
@click.option('-l', '--location_id', help='Restrict list to location Id')
@click.option('-c', '--csvfile', help='Save results to CSV file.')
def devices(csvfile, location_id):
    """ List devices in given location. """
    devicesDF=wbxdf.devicesDF(location_id)
    devicesDF.print(csvfile)      


@click.command()
@click.argument('device_id')
@click.argument('name')
def device_status(device_id, name):
    """ Show device status. """
    data=wbxr.get_wbx_data(f"xapi/status", f"?deviceId={device_id}&name={name}")
    pprint(data)        


def print_metrics(workspace_id, metric, fmt):
    metricDF=wbxdf.metricsDF(workspace_id, metric)
    metricDF.print(fmt)


@click.command()
@click.argument('metric')
@click.option('-l', '--location_id', help='Get metrics data for all workspaces under location ID')
@click.option('-w', '--workspace_id', help='Get metrics data for specific workspace ID')
# @click.option('-f', '--fmt', help='Save to CSV or JSON file.')
@click.option('-a', '--aggreate', is_flag=True, help='Aggreate workspaces data in a single file. Only applicable to if --location_id is selected')
def metrics(metric, aggreate=False, location_id="", workspace_id=""):
    """ Gather yesteray's hourly peopleCount or timeUsed metric for a workspace or workspaces in a location.
    """
    if ( not (location_id or workspace_id) ):

        print ( "I need a location or a workspace ID")
        return (400)
    
    match metric:
        case 'peopleCount':
            pass
        case 'timeUsed':
            pass
        case _ :
            print(f"{metric} value not supported")
            return(400)
        
    if (workspace_id):
        print_metrics( workspace_id, metric, 'JSON' )

    elif (location_id):
        aggreate_data=[]
        workspacesDF=wbxdf.workspacesDF(location_id)
        workspaces=workspacesDF.jsonList['items']
        for workspace in workspaces :
            workspace_id = workspace['id']
            if ( aggreate ):
                print(f"Fetching metrics for Workspace {workspace_id}")
                item = {}
                metricsDF=wbxdf.metricsDF(workspace_id, metric)
                item[metric] = metricsDF.jsonList
                item['workspace'] = workspace
                aggreate_data.append(item)
            else :
                print_metrics( workspace_id, metric, 'JSON' )
        if ( aggreate ):
            frm = wbx_utils.midnight_iso_ms(1)
            fn=f"{metric}_{location_id}_{frm}.json"
            with open(fn, "w") as jsfile:
                jsfile.write(json.dumps(aggreate_data, indent=2))
                print(f"Created {fn}")
            
    
#####################
### Top Lev       ###
#####################

@click.group()
@click.version_option(__version__)
@click.option('-t', '--token', help='Your access token. Read from AUTH_BEARER env variable by default. You can find your personal token at https://developer.webex.com/docs/getting-started.')
@click.option('-d', '--debug', default=2, help='Debug level.')
def cli(debug, token):
    wbx_utils.DEBUG_LEVEL = debug
    if (debug >=3 ):
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
    if (token):
        # wbxr.set_token(token)
        wbx.ACCESS_TOKEN=token
    else:
        if ( 'AUTH_BEARER' in os.environ ):
            ut.trace(3, f"setting Access Token from env {os.environ['AUTH_BEARER']}")
            wbx.ACCESS_TOKEN=os.environ['AUTH_BEARER']
        else:
            sys.exit('No access token set. Use option -t or AUTH_BEARER env variable')


cli.add_command(metrics)
cli.add_command(locations)
cli.add_command(workspaces)
cli.add_command(devices)
cli.add_command(device_status)

if __name__ == '__main__':
    cli()
