import base64
import json
# From USB capture
challenge ="D5CxgaFPGIQu5fGYPEjo-YA9Dqd6y2PBoWP6p56TpFw"
signature ="010000000030460221009683e1a139967409c2873dfdf65f770545858ea37b362bb28b12d6d38cccf442022100dcd87355102194001255c534f40737a56b147a9b40dc9f3594388627fc28195d"
# Craft response
clientData = base64.b64encode(('{"challenge":"'+challenge+'","origin":"https://x-factor.france-cybersecurity-challenge.fr","typ":"navigator.id.getAssertion"}').encode()).replace(b"/", b"_").replace(b"+", b"-").replace(b"=", b"").decode()
keyHandle ="MiXECXjEbxAAe7QOH2gsiNiK7bXeuGJnLUGO7kbJutdODZvuqV-T1TPpTVEVIrynmScyNOjQaRAUi0PSH8LUtQ"
signatureData = base64.b64encode( bytes.fromhex( signature )).replace(
b"/", b"_").replace(b"+", b"-").replace(b"=", b"").decode()
print( json.dumps({
"clientData": clientData ,
"keyHandle": keyHandle ,
"signatureData": signatureData
}))
