'''
This script is provided free of charge by doth.fr. We hope such scripts are
helpful when used in conjunction with Extreme products and technology and can
be used as examples to modify and adapt for your ultimate requirements.
doth.fr will not provide any official support for these scripts.
ANY SCRIPTS PROVIDED BY DOTH.FR ARE HEREBY PROVIDED \"AS IS\", WITHOUT WARRANTY
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL EXTREME OR ITS THIRD PARTY LICENSORS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE USE OR DISTRIBUTION OF SUCH
SCRIPTS.
Using Ludovico Steven XMC-Lib :
https://github.com/extremetme/XMC-LudoLib/

Version 1.0 : initial release of script
'''

#

##########################################################
# XMC Script: Port_Speed_and_Duplex                      #
# Written by Olivier Martin, doth.fr                     #
##########################################################

__version__ = '1.0'

'''
#@MetaDataStart
#@DetailDescriptionStart
#This script permits to change auto-negotiation state
#and then configure speed and duplex.
#Works on VOSS/Fabric Engines only
#@DetailDescriptionEnd
#@SectionStart (description = \"Auto negotiation\")
#    @VariableFieldLabel (
#        description = \"Auto negotiation: set port auto-negotiation state\",
#        type = string,
#        required = yes,
#        validValues = [Enabled, Disabled],
#        name = \"userInput_autoneg\",
#    )#@SectionEnd
#@SectionStart (description = \"Speed and duplex (if needed)\")
#    @VariableFieldLabel (
#        description = \"Speed: set port speed if auto-negotiation is disabled\",
#        type = string,
#        required = no,
#        validValues = [10, 100, 1000],
#        name = \"userInput_speed\",
#    )
#    @VariableFieldLabel (
#        description = \"Duplex: set port duplex if auto-negotiation is disabled\",
#        type = string,
#        required = no,
#        validValues = [Half, Full],
#        name = \"userInput_duplex\",
#    )
#@SectionEnd
#@SectionStart (description = \"Sanity / Debug\")
#    @VariableFieldLabel (
#        description = \"Sanity: enable if you do not trust this script and wish to first see what it does. In sanity mode config commands are not executed\",
#        type = string,
#        required = no,
#        validValues = [Enable, Disable],
#        name = \"userInput_sanity\",
#    )
#    @VariableFieldLabel (
#        description = \"Debug: enable if you need to report a problem to the script author\",
#        type = string,
#        required = no,
#        validValues = [Enable, Disable],
#        name = \"userInput_debug\",
#    )
#@SectionEnd
#@MetaDataEnd
'''

# Global variables
Debug = False    # Enables debug messages
Sanity = False   # If enabled, config commands are not sent to host (show commands are operational)

# Import Ludovico's scripts
pathToScripts = "/usr/local/Extreme_Networks/NetSight/appdata/scripting/overrides"
execfile(pathToScripts+"/cli.py")
execfile(pathToScripts+"/base.py")


#
# MAIN:
#
def main():
    #
    # INIT: Init variables flags based on input combos
    #
    #Sanity
    try:
        if emc_vars['userInput_sanity'].lower() == 'enable':
            Sanity = True
        elif emc_vars['userInput_sanity'].lower() == 'disable':
            Sanity = False
    except:
        pass
    #Debug
    try:
        if emc_vars['userInput_debug'].lower() == 'enable':
            Debug = True
        elif emc_vars['userInput_debug'].lower() == 'disable':
            Debug = False
    except:
        pass

    # Set default value
    portSpeed = "10"
    portDuplex = "half"

    # Write Version of script and server
    print "{} version {} on XIQ-SE/XMC version {}".format(scriptName(), __version__, emc_vars["serverVersion"])

    # Activate autonegotiation
    if emc_vars['userInput_autoneg'].lower() == 'enabled':
        for port in emc_vars["port"].split(','):
            print "Configuring port "+port
            configCmds = '''
enable;
configure terminal;
interface gigabit {};
auto-negotiate port {} enable;
'''.format(port,port)
            sendCLI_configChain(configCmds)
    else:
        for port in emc_vars["port"].split(','):
            print "Configuring port "+port
            # Set values
            if emc_vars['userInput_speed']:
                portSpeed = emc_vars['userInput_speed']
            print "Set speed to " + portSpeed
            if emc_vars['userInput_duplex']:
                portDuplex= emc_vars['userInput_duplex']
            print "Set duplex to " + portDuplex

            configCmds = '''
enable;
configure terminal;
interface gigabit {};
no auto-negotiate port {} enable;
speed {};
duplex {};
'''.format(port,port, portSpeed, portDuplex)
            sendCLI_configChain(configCmds)

    print ("End of script")

main()
