## Architecture

### http Status responses are check automatically
base_client.py will raise an exception on any non 2XX response.




## Note
for the sake of simplicity, the api_models send objects in a hard-coded way.

Best practice would be to have the objects (like `game_service`, `payment_service` etc) have methods to serialize and de-serialize, so we can pass objects "as-is" to the api client (adding to/from_dict() methods to the objects).

This way we would also have automatic way to validate the responses of the APIs (as we would turn it back into the objects).


## Extras
1) we could acrhitect api_model to expect user_id on initialization (so it will automatically validate that the response is with the correct user_id)

2) we could have the api models auto validate the STATUS, and raise an exception on bad STATUSes?