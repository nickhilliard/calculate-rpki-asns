#!/usr/bin/env python3
#
# calculate-rpki-asns.py - script to calculate RPKI usage in a set of ASNs
#

import sys, io, os
import argparse, json, re
import urllib.request, urllib.error

from pprint import pprint

def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('-u', '--url', help='IXP Manager URL', nargs='+', required=False)
  parser.add_argument('-a', '--asn', help='IXP Manager URL', nargs='+', required=False)
  parser.add_argument('-d', '--debug', help='Enable debugging', action='store_true', required=False)

  args = parser.parse_args()

  usesrpki = {}

  if (args.asn):
    asnlist = args.asn
  else:
    try:
      args.url[0]
    except TypeError:
      print ('No ASNs or IXP Manager API URL provided. Quitting.')
      exit (1)

    ixpmanagerurl = re.sub("\/{1,}$", "", args.url[0]) + '/api/v4/member-export/ixf/1.0'
    if (args.debug):
      print ("DEBUG: opening IXP Manager API at " + ixpmanagerurl)
    url = open_url(ixpmanagerurl)
    data = json.load(url)

    asnlist = []
    for member in data['member_list']:
      asnlist.append(str(member['asnum']))

  for member in asnlist:
    memberusesrpki = 0
    asn = str(member)
    irrexplorerurl = 'https://irrexplorer.nlnog.net/api/prefixes/asn/AS' + asn

    if (args.debug):
      print ("DEBUG: opening IRR Explorer API at " + irrexplorerurl)

    irrurl = open_url(irrexplorerurl)
    if (irrurl is None):
      continue

    irrexplorer = json.load(irrurl)
    try:
      irrexplorer['directOrigin']
    except NameError:
      print ('AS' + asn + ' did not return valid data on IRR Explorer.')
      continue

    for directorigin in irrexplorer['directOrigin']:
      for rpkiroutes in directorigin['rpkiRoutes']:
        if (rpkiroutes['rpkiStatus'] == 'VALID'):
          usesrpki[asn] = 1
          continue

    if (args.debug):
      if (asn in usesrpki.keys()):
        print ("DEBUG: AS" + asn + ' has RPKI ROAs.')
      else:
        print ("DEBUG: AS" + asn + ' has no RPKI ROAs.')

  rpkiusers = len(usesrpki)
  ixpconnected = len(asnlist)

  print('Number of IXP Members using RPKI: ' + str(rpkiusers))
  print('Total number of ASNs considered:  ' + str(ixpconnected))
  print('Percentage of parties using RPKI: ' + str(int(rpkiusers / ixpconnected * 100)) + '%')

def open_url(request):
  try:
    return urllib.request.urlopen(request)
  except urllib.error.HTTPError as e:
    return None

if __name__ == "__main__":
  main()
