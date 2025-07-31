# Test Design
TODO: write how i imagine the user flow


## Positive test cases

### 1) Valid Game (WIN)
**Preconditions:** User with Id 123 has a balance of $150.

```txt
1 GET /user/balance?userId=123   --->   User has $150

2 POST /payment/placeBet with betAmount=10   --->   transactionId

2.1 GET /user/balance?userId=123   --->   User has $140 (OPTIONAL STEP)

3. POST /slot/spin with betAmount + transactionId from step 2   --->   winAmount=N (SIMULATED OUTCOME: WIN)

4. POST /payment/payout   --->   verify "newBalance" == (150 - 10) + N

5. GET /user/balance?userId=123   --->   verify "balance" == (150 - 10) + N
```

### 2) Valid Game (LOSE)
**Preconditions:** User with Id 123 has a balance of $150.

```txt
1 GET /user/balance?userId=123   --->   User has $150

2 POST /payment/placeBet with betAmount=10   --->   transactionId

2.1 GET /user/balance?userId=123   --->   User has $140 (OPTIONAL STEP)

3. POST /slot/spin with betAmount + transactionId from step 2   ---> SIMULATED OUTCOME: LOSE

4. GET /user/balance?userId=123   --->   verify "balance" == (150 - 10) == $140 
```

### 3) Betting all the User balance (and losing)
**Preconditions:** User with Id 123 has a balance of $150.
```txt
1 GET /user/balance?userId=123   --->   User has $150

2 POST /payment/placeBet with betAmount=150   --->   transactionId

2.1 GET /user/balance?userId=123   --->   User has $0 (OPTIONAL STEP)

3. POST /slot/spin with betAmount + transactionId from step 2   --->   SIMULATED OUTCOME: LOSE

4. GET /user/balance?userId=123   --->   verify "balance" == 0
```




## Negative test cases
### 1) Placing a bet with 0 balance
**Preconditions:** User with Id 123 has a balance of $0.

```txt
1 GET /user/balance?userId=123   --->   User has $0

2 POST /payment/placeBet with betAmount=10   --->   Error of zero balance/insufficient funds?

3 GET /user/balance?userId=123   --->   Still has $0
```

(also should test betting $0 with $0 balance (is it a negative or an edge case?))


### 2) Non-existing User
**Preconditions:** Choose a non existing Id (check against db?)
```txt
1 GET /user/balance?userId={NON_EXISTING_ID}   --->   Error (404?)
```

### 3) Placing a negative bet
**Preconditions:** User with Id 123 has a balance of $150.

```txt
1 GET /user/balance?userId=123   --->   User has $150

2 POST /payment/placeBet with betAmount=-10   --->   Error of invalid bet?

3 GET /user/balance?userId=123   --->   Still has $150
```

### 4) Re-using transaction Id (transactionId is invalid after it was used)
**Preconditions:** User with Id 123 has a balance of $150.

```txt
1 GET /user/balance?userId=123   --->   User has $150

2 POST /payment/placeBet with betAmount=-10   --->   transactionId

2.1 GET /user/balance?userId=123   --->   User has $140 (OPTIONAL STEP)

3. POST /slot/spin with betAmount + transactionId from step 2   --->   Any 200 response

4 GET /user/balance?userId=123   --->   User has the correct balance after calculation of step 3 

5. POST /slot/spin with betAmount + transactionId from step 2   --->   Error regarding the reusing of transactionId 

6. GET /user/balance?userId=123   --->   User has the same balance as in step 4
```

### 5) Notify without a message
**Preconditions:** User with Id 123, had balance, placed a bet and triggered a spin.

```txt
1. POST /notify + transactionId from Preconditions + without message   --->   Error regarding missing message/message is required
```

(what about message as an empty string?)

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
1) Sending /notify before triggering a spin
2) placing bets lower than minimum/higher than maximum (if there is min/max at all)