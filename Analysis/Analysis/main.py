from BranchVisit.branchVisit import branchVisit


with branchVisit() as bot: # teardown=True can be set in branchVisit()
    bot.land_first_page()
    bot.log_in()
    bot.deposit_card()
    bot.crm_deposit_rate()