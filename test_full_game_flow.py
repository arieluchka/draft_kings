import pytest
from common.models import *

WIN_MESSAGE_FORMAT = "Congratulations! You won ${win_amount}!" # optionally we can have a central file for such templates
LOSE_MESSAGE_FORMAT = "Better luck next time!"



# ideally we will have a set-up + cleanup functions to set the user and balance
@pytest.mark.parametrize("test_params",[
    (123, 150, 10),
    (555, 10, 2)
])
def test_full_game_flow(test_params, casino_api):
    user_id, starting_balance, initial_bet = test_params

    assert casino_api.user_service.get_balance(user_id=user_id) == starting_balance, "The User didn't start with the expected balance"

    bet_res = casino_api.payment_service.place_bet(
        request=PlaceBetRequest(
            userId=user_id,
            betAmount=initial_bet
        )
    )
    assert bet_res.status == TransactionStatus.SUCCESS, f"placeBet didn't return status SUCCESS (actual status: {bet_res.status})"

    expected_balance_after_bet = starting_balance - initial_bet
    assert bet_res.newBalance == expected_balance_after_bet, f"expecting balance to be {expected_balance_after_bet}, but the actual response was {bet_res.newBalance}"

    transaction_id = bet_res.transactionId
    spin_res = casino_api.game_service.spin_slot(
        SlotSpinRequest(
            userId=user_id,
            transactionId=transaction_id,
            betAmount=initial_bet
        )
    )

    win_amount = spin_res.winAmount

    if spin_res.outcome == GameOutcome.WIN:
        assert win_amount > initial_bet
        assert spin_res.message == WIN_MESSAGE_FORMAT.format(win_amount=win_amount), "Got an unexpected message."

        payout_res = casino_api.payment_service.process_payout(
            PayoutRequest(
                userId=user_id,
                transactionId=transaction_id,
                winAmount=win_amount
            )
        )
        assert payout_res.status == TransactionStatus.SUCCESS
        assert payout_res.newBalance == win_amount + expected_balance_after_bet


    elif spin_res.outcome == GameOutcome.LOSE:
        assert win_amount == 0
        assert spin_res.message == LOSE_MESSAGE_FORMAT, "Got an unexpected message."

    else:
        pytest.fail(f"GameOutcome from the Spin api response was not WIN nor LOSE. actual valud: {spin_res.outcome}")

    notification_res = casino_api.notification_service.send_notification(
        NotificationRequest(
            userId=user_id,
            transactionId=transaction_id,
            message=spin_res.message
        )
    )
    assert notification_res.status == NotificationStatus.SENT