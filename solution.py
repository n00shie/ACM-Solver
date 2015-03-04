import sys
import pdb;

def main():
	cases = []
	with open("input.txt") as f:
		case_entry = {}
		for line in f:
			args = line.split()
			
			if len(args) is 0:
				continue

			if len(args) is 3:
				if(len(case_entry) is not 0):
					cases.append(case_entry)
				case_entry = {"machines": [], "cash": int(args[1]), "days": int(args[2])}
				
			elif len(args) is 4:
				machine = { "day": int(args[0]), "price": int(args[1]), "resale": int(args[2]), "profit": int(args[3]) }
				case_entry["machines"].append(machine)
		# append last case_entry
		cases.append(case_entry)
		
	for idx, case in enumerate(cases):
		c = total_cash(case["machines"], case["cash"], case["days"])
		print "Case {}: {}".format(idx + 1, c)


def total_cash(machines, cash, days):
	# sort machines by day
	machines.sort()
	previous_day = 1
	total_cash = cash
	owned_machine = {}
	day_array = set(map(lambda x: x["day"], machines))
	for cur_day in day_array:
		# find other machines that are available for purchase in the same day
		purchace_candidates = filter(lambda m: m["day"] == cur_day, machines)
		resale_value = 0
		
		# collect profits from currently owned machine
		if len(owned_machine) is not 0:
			total_cash += (cur_day - previous_day) * owned_machine["profit"]
			resale_value = owned_machine["resale"]
		
		# pdb.set_trace()

		# filter out candidates we can't afford
		purchace_candidates = filter(lambda m: m["price"] <= (total_cash + resale_value), purchace_candidates)

		if len(purchace_candidates) is not 0:
			# Candidate utility is the projected the total cash amount we will 
			# have at the end of the restructuring period, taking into account
			# candidate's purchase, and resale price, as well as current machine's 
			# resale price. The assumption is no other purchases will be made after.
			
			# In practice, since total_cash and owned_machine["resale"] would 
			# appear in both utility calculations for the candidate and owned 
			# machine, we can take them out of the utility calculation

			candidates_utility = map(lambda candidate: (days - cur_day) * candidate["profit"] - candidate["price"] + candidate["resale"], purchace_candidates)
			best_candidate_utility = max(candidates_utility)
			new_machine = purchace_candidates[candidates_utility.index(best_candidate_utility)]
			if len(owned_machine) is not 0:
				current_utility = (days - cur_day) * owned_machine["profit"]
				if best_candidate_utility > current_utility:
					total_cash += (owned_machine["resale"] - new_machine["price"])
					owned_machine = new_machine
			else:
				owned_machine = new_machine
				total_cash -= owned_machine["price"]

		previous_day = cur_day
	if len(owned_machine) is not 0:
		total_cash += owned_machine["resale"]
		total_cash += (days - cur_day) * owned_machine["profit"]

	return total_cash


if __name__ == '__main__': 
  main()