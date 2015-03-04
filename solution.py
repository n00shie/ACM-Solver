import sys

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
				case_entry = {"machines": [], "cash": args[1], "days": args[2]}
				
			elif len(args) is 4:
				case_entry["machines"].append(args)

	case_num = 1
	for case in cases:
		c = total_cash(case["machines"], case["cash"], case["days"])
		print "Case " + case_num + ":" + c

if __name__ == '__main__': 
  main()