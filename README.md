# calculate-rpki-asns

Given a list of ASNs, or a feed from IXP Manager, this script calculates how many ASNs use have ROAs defined.

# Usage

    # python3 calculate-rpki-asns.py --debug -a 2128 112 42 43760
    DEBUG: opening IRR Explorer API at https://irrexplorer.nlnog.net/api/prefixes/asn/AS2128
    DEBUG: AS2128 has no RPKI ROAs.
    DEBUG: opening IRR Explorer API at https://irrexplorer.nlnog.net/api/prefixes/asn/AS112
    DEBUG: AS112 has no RPKI ROAs.
    DEBUG: opening IRR Explorer API at https://irrexplorer.nlnog.net/api/prefixes/asn/AS42
    DEBUG: AS42 has RPKI ROAs.
    DEBUG: opening IRR Explorer API at https://irrexplorer.nlnog.net/api/prefixes/asn/AS43760
    Number of IXP Members using RPKI: 1
    Total number of ASNs considered:  4
    Percentage of parties using RPKI: 25% 

To pull a list from IXP Manager:

    # python3 calculate-rpki-asns.py --url https://www.inex.ie/ixp/
    Number of IXP Members using RPKI: 90
    Total number of ASNs considered:  113
    Percentage of parties using RPKI: 79%
