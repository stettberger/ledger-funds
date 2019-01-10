export LEDGER_FILE?=ledger.dat
export LEDGER_DATE_FORMAT=%d.%m.%Y
LEDGER=ledger --color --force-color --strict

P="this-month"

all: all-this-month

all-this-month: register-this-month balance funds budget-this-month
all-last-month: register-last-month balance funds budget-last-month


overview: budget-this-month funds balance

balance:
	@echo "=================== Balance ======================="
	@echo
	@${LEDGER} bal assets liabilities
	@echo

funds:
	@echo "=================== Funds  ======================="
	@./main.py funds
	@echo


budget: budget-last-month budget-this-month

budget-%:
	@echo '=================== Budget ($(subst -, ,$(patsubst budget-%,%,$@))) ========================'
	@${LEDGER} budget -p "$(subst -, ,$(patsubst budget-%,%,$@))" \
            -E \( funds or expenses \) and  not '%automatic'
	@echo
	@echo

register: register-from-last-month-to-next-month

register-%:
	@echo '=================== Register ($(subst -, ,$(patsubst budget-%,%,$@))) ========================'
	@echo
	@${LEDGER} register -p "$(subst -, ,$(patsubst register-%,%,$@))" not assets
	@echo

demo:
	@${LEDGER} -f ledger-demo.dat -G -V bal
