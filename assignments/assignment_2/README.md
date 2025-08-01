## Architecture

### API client interfaces ([go to folder](/common/api_models))

each service has a high level API client, to allow a cental and unanimous way of communicating with the services.

If there will be any change to the apis, we will have to change/modify it only in one place.

### Request and Response objects ([go to folder](/common/models))

All data in/from the API is objectified, to avoid user error when accessing attributes (accidentaly writing `WinAmount` instead of `winAmount`), and providing IDE suggestions.

Also, will allow us to add to_json from_json (to serialize for api requests/from api responses), and we could also use pydantic to automatically validate the structure of response from the APIs.

### http Status responses are check automatically ([go to file](/common/api_models/base_client.py))

base_client.py will raise an exception on any non 2XX response. 

### Central hosts.py file with all service urls ([go to file](/common/hosts.py))

### Conftest file has a Session scoped fixture that returns the CasinoApi object for all tests ([go to file](/conftest.py))

(session scope allows us to create a single object, that all tests will use)

### Test designed to support parameterized execution ([go to file](/test_full_game_flow.py))
This way we can easily re-use this test for multiple test-cases, involving different users/pre-conditions.

<br>

You can execute `pytest --collect-only -c .\pytest.ini` from the root directory to see the parameterization.

## Note
for the sake of simplicity, the api_models send objects in a hard-coded way.

Best practice would be to have the objects (like `game_service`, `payment_service` etc) have methods to serialize and de-serialize, so we can pass objects "as-is" to the api client (adding to/from_dict() methods to the objects).

This way we would also have automatic way to validate the responses of the APIs (as we would turn it back into the objects).


## Extras
1) we could acrhitect api_model to expect user_id on initialization (so it will automatically validate that the response is with the correct user_id)

2) we could have the api models auto validate the STATUS, and raise an exception on bad STATUSes?