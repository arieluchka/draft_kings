# Test Design
TODO: write how i imagine the user flow


## Positive test cases

### 1) Valid Game (WIN)
**Preconditions:** User with Id 123 has a balance of $150.

User with enough balance, places a valid bet and wins the game.
The winnings are correctly added to his balance.

<details>
  <summary>API calls logic example</summary>

```txt
1 GET /user/balance?userId=123   --->   User has $150

2 POST /payment/placeBet with betAmount=10   --->   transactionId

2.1 GET /user/balance?userId=123   --->   User has $140 (OPTIONAL STEP)

3. POST /slot/spin with betAmount + transactionId from step 2   --->   winAmount=N (SIMULATED OUTCOME: WIN)

4. POST /payment/payout   --->   verify "newBalance" == (150 - 10) + N

5. GET /user/balance?userId=123   --->   verify "balance" == (150 - 10) + N
```
</details>

### 2) Valid Game (LOSE)
**Preconditions:** User with Id 123 has a balance of $150.

User with enought balance, places a valid bet and loses the game. His initial balance is subtracted only by the bet he placed.

<details>
  <summary>API calls logic example</summary>

```txt
1 GET /user/balance?userId=123   --->   User has $150

2 POST /payment/placeBet with betAmount=10   --->   transactionId

2.1 GET /user/balance?userId=123   --->   User has $140 (OPTIONAL STEP)

3. POST /slot/spin with betAmount + transactionId from step 2   ---> SIMULATED OUTCOME: LOSE

4. GET /user/balance?userId=123   --->   verify "balance" == (150 - 10) == $140 
```
</details>

### 3) Betting all the User balance (and losing)
**Preconditions:** User with Id 123 has a balance of $150.

User with a positive balance, places a bet the size of his entire balance.
The balance is subtracted and is now 0!

After the game ends he lost, balance is still 0.

<details>
  <summary>API calls logic example</summary>


```txt
1 GET /user/balance?userId=123   --->   User has $150

2 POST /payment/placeBet with betAmount=150   --->   transactionId

2.1 GET /user/balance?userId=123   --->   User has $0 (OPTIONAL STEP)

3. POST /slot/spin with betAmount + transactionId from step 2   --->   SIMULATED OUTCOME: LOSE

4. GET /user/balance?userId=123   --->   verify "balance" == 0
```

</details>

### 4) Betting all the User balance (and winning)

User with a positive balance, places a bet the size of his entire balance.
After the bet, the balance is subtracted and is now 0!

After the game ends he wins, balance is now higher than his initial balance.

### 5) Notification and Spin messages (in a WIN)

In a winning round, the message from the SPIN response (after a win) is `"Congratulations! You won $N!"`.

Verify it is the same message that is sent to the notification service.

## Negative test cases
### 1) Placing a bet with 0 balance
**Preconditions:** User with Id 123 has a balance of $0.

User with 0 balance tries to place a bet.

An error message is showed, the spin doesn't proceed, the balance didnt change.

<details>
  <summary>API calls logic example</summary>

```txt
1 GET /user/balance?userId=123   --->   User has $0

2 POST /payment/placeBet with betAmount=10   --->   Error of zero balance/insufficient funds?

3 GET /user/balance?userId=123   --->   Still has $0
```

(also should test betting $0 with $0 balance (is it a negative or an edge case?))
</details>


### 2) Non-existing User
**Preconditions:** Choose a non existing Id (check against db?)

All services and api endpoints are called with a non-existing user id.

An error message with a 4XX (404?) is expected.

<details>
  <summary>API calls logic example</summary>

```txt
1 GET /user/balance?userId={NON_EXISTING_ID}   --->   Error (404?)
```
</details>

### 3) Placing a negative bet
**Preconditions:** User with Id 123 has a balance of $150.

User tries to place a bet of a negative value.
An error message is raised, the bet doesn't proceed, the balance is unchanged.

<details>
  <summary>API calls logic example</summary>

```txt
1 GET /user/balance?userId=123   --->   User has $150

2 POST /payment/placeBet with betAmount=-10   --->   Error of invalid bet?

3 GET /user/balance?userId=123   --->   Still has $150
```
</details>

### 4) Re-using transaction Id for extra payout (transactionId is invalid after it was used)
**Preconditions:** User with Id 123 has a balance of $150.

The user has sufficient balance, places a valid bet.

The spin goes through and he WINS, and gets a payout. (balance changes)

He then tries to invoke a spin/payout with the same transaction ID.

An error message is raised, and the balance is unchanged.

<details>
  <summary>API calls logic example</summary>

```txt
1 GET /user/balance?userId=123   --->   User has $150

2 POST /payment/placeBet with betAmount=-10   --->   transactionId

2.1 GET /user/balance?userId=123   --->   User has $140 (OPTIONAL STEP)

3. POST /slot/spin with betAmount + transactionId from step 2   --->   Any 200 response

4 GET /user/balance?userId=123   --->   User has the correct balance after calculation of step 3 

5. POST /slot/spin with betAmount + transactionId from step 2   --->   Error regarding the reusing of transactionId 

6. GET /user/balance?userId=123   --->   User has the same balance as in step 4
```
</details>

### 5) Notify without a message
**Preconditions:** Valid user with balance, placed a bet and Spinned successfully. using the transactionId....

The /notify endpoint is invoked with a valid transactionId but without a message.

an error is rasied that the message is required.

<details>
  <summary>API calls logic example</summary>

```txt
1. POST /notify + transactionId from Preconditions + without message   --->   Error regarding missing message/message is required
```
(what about message as an empty string?)

</details>


## Edge case
### Concurrent Bets
**Preconditions:** User with Id 123 has a balance of $150.

The user concurrently bet and spin (opens multiple tabs/different computers?) 3 times with a betAmount of $50.

**Expected Result:**

All bets went through (3 seperate transactionId)
before the spins were concluded, balance is showed as 0.
User received 3 notifications with different notificationId.

**importance**

This test verifys that the system is able to handle multiple flows for the same user seperatly, without it affecting one another.
Also, we verify that the balance is updated immediatly after each bet placement.

## Extras
1) Sending /notify before triggering a spin (with a valid transaction Id)
2) placing bets lower than minimum/higher than maximum (if there is min/max at all)