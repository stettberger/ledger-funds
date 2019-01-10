Ledger CLI with Budget and Funds
================================

I organize my personal finance with
[ledger-cli](https://www.ledger-cli.org/) which supports a myriads of
basic features that can be used to build workflows for your financial needs.

One particular useful feature is monthly budgeting. It helps you to
get a feeling how much you already spent on a particular expense in
the current month. However, not all expenses can be pressed into the
form of a monthly budget but they are part of a larger investment
vision. For example, if you save your excess money at the end of the
month to go on vacaction once a year. How do you track your current
level of savings for your vacaction.

In this example ledger file, I present you a method to use **funds**
alongside the normal monthly budgeting. Funds are virtual accounts
that are filled manually with money by you. Expenses to certain normal
`Expenses:` accounts automatically drain money from a fund.

Please open the `ledger.dat` file for the coming details.

Fill the Fund
=============

First, we define a few funds that we want to use to track investements
plan that span multiple months.

     account Funds:Travel
     account Funds:Saving
     account Funds:Sporadic

At the end of the month, or whenever you feel like it, you transfer
money virtually to these accounts. These transfers are accounted in
the ledger monthly budget and you see that you "spent" money on your
funds.

    2019/01/31 Closing
        (Funds:Saving)                               200 €
        (Funds:Sporadic)                           25.59 €


The Automatic Fund Transaction
=====================================

If we want drain money from a fund, we want to do it automatic.
Furthermore, these drains may not influence the current monthly budget
as they were already considered in another month in the budget.

Therefore, we specify some accounts that are automatically connected
to a fund. Furthermore, all transactions in these accounts are marked
as 'automatic', which we will consider in the budget expression.

    account Expenses:Travel:19:San Francisco
    account Expenses:Travel:19:35C3

    = /Expenses:Travel:/
        (Funds:Travel)                                -1 ; :automatic:

In order to get a proper budget, we have to exclude the automatic tagged transactions:

     ledger -f ledger.dat -p "this month" budget \( expenses or funds \) and not %automatic

As a companion for the fund mechanism, this repo also containts a
`main.py` file that displays the development of accounts (also fund
accounts) for this month and the last month.

Output for January 2019 for ledger.dat
======================================

    =================== Register (register this month) ========================

    01.01.2019 My Corporation                Income:Salary                           -2,000.00 €       -2,000.00 €
    02.01.2019 Rent and Electricity          Expenses:Flat:Rent                         630.00 €       -1,370.00 €
                                             Expenses:Flat:Others                        50.00 €       -1,320.00 €
    12.01.2019 Travel to San Francisco       Expenses:Travel:19:San Francisco           325.00 €         -995.00 €
                                             (Funds:Travel)                            -325.00 €       -1,320.00 €
    31.01.2019 Closing                       (Funds:Saving)                             200.00 €       -1,120.00 €
                                             (Funds:Sporadic)                            25.59 €       -1,094.41 €

    =================== Balance =======================

              5,995.00 €  Assets

    =================== Funds  =======================
           Total   This Month   Last Month
        200.00 €     200.00 €            0 Funds:Saving
         25.59 €      25.59 €            0 Funds:Sporadic
        350.00 €    -325.00 €     675.00 € Funds:Travel

    =================== Budget (this month) ========================
        680.00 €   1,774.41 €  -1,094.41 €   38%  Expenses
        680.00 €     704.95 €     -24.95 €   96%    Flat
         50.00 €      74.95 €     -24.95 €   67%      Others
        630.00 €     630.00 €            0  100%      Rent
               0   1,069.46 €  -1,069.46 €     0    Misc
        225.59 €     225.59 €            0  100%  Funds
        200.00 €     200.00 €            0  100%    Saving
         25.59 €      25.59 €            0  100%    Sporadic
               0            0            0     0    Travel
    ------------ ------------ ------------ -----
        905.59 €   2,000.00 €  -1,094.41 €   45%
