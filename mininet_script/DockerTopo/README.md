# REST requests
## GET Requests
### Switches
`http://172.16.117.50:9110/stats/switches`
### Description of switches
`http://172.16.117.50:9110/stats/desc/1`
### Flow entries of switches
`http://172.16.117.50:9110/stats/flow/1`
### Mactable of Switches
`http://172.16.117.50:9110/simpleswitch/mactable/0000000000000001`

## POST Requests
### View flow with filter
`curl -d '{"out_port":2}' -X POST http://172.16.117.50:9110/stats/flow/1`
### Add new flow
`curl -d '{"dpid": 1,"cookie": 42,"priority": 45000,"match": {"in_port": 3},"actions": []}' -X POST http://172.16.117.50:9110/stats/flowentry/add`
### Delete new flow
`curl -d '{"dpid": 1,"cookie": 42,"priority": 45000,"match": {"in_port": 3},"actions": []}' -X POST http://172.16.117.50:9110/stats/flowentry/delete_strict`