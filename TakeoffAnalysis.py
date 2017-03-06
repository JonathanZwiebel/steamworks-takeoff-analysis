import TBAConnection

week = 1

total_takeoff_calculated = 0
total_takeoff_known = 3214

total_points_calculated = 0
total_points_known = 490330

# array[greater][lesser]
total_count = [[0],[0,0],[0,0,0],[0,0,0,0]]
higher_win_count = [[0],[0,0],[0,0,0],[0,0,0,0]]
tie_count = [[0],[0,0],[0,0,0],[0,0,0,0]]
lower_win_count = [[0],[0,0],[0,0,0],[0,0,0,0]]

events = TBAConnection.get_event_list()
for event in events:
	if event.get_week() == week and event.get_key() != "2017isde1":
		print event.get_key() + " of type " + event.get_event_type()
		matches = TBAConnection.get_matches(event.get_key())
		for match in matches:
			if not match.is_bad() and match.get_level() == "qm":
				blue_takeoffs, red_takeoffs = match.get_takeoffs()
				total_takeoff_calculated += blue_takeoffs
				total_takeoff_calculated += red_takeoffs

				blue_total, red_total = match.get_totals()
				total_points_calculated += blue_total
				total_points_calculated += red_total

				if blue_takeoffs < red_takeoffs:
					greater_takeoff_count = red_takeoffs
					lesser_takeoff_count = blue_takeoffs
					more_takeoffs = "red"
				elif red_takeoffs < blue_takeoffs:
					greater_takeoff_count = blue_takeoffs
					lesser_takeoff_count = red_takeoffs
					more_takeoffs = "blue"
				else:
					greater_takeoff_count = lesser_takeoff_count = red_takeoffs
					more_takeoffs = "tie"

				if blue_total < red_total:
					winning_score = red_total
					losing_score = blue_total
					winner = "red"
				elif red_total < blue_total:
					winning_score = blue_total
					losing_score = red_total
					winner = "blue"
				else:
					winning_score = losing_score = red_total
					winner = "tie"
				winning_margin = winning_score - losing_score


				total_count[greater_takeoff_count][lesser_takeoff_count] += 1
				if winner == "tie":
					tie_count[greater_takeoff_count][lesser_takeoff_count] += 1
				elif winner == more_takeoffs:
					higher_win_count[greater_takeoff_count][lesser_takeoff_count] += 1
				else:
					lower_win_count[greater_takeoff_count][lesser_takeoff_count] += 1




print total_takeoff_calculated
assert total_takeoff_calculated == total_takeoff_known
print total_points_calculated
assert total_points_known - total_points_calculated < 10 and total_points_known - total_points_calculated > -10

print "Total Count: " + str(total_count)
print "Tied Games: " + str(tie_count)
print "Games where the higher takeoff alliance wins: " + str(higher_win_count)
print "Games where the lower takeoff alliance wins: " + str(lower_win_count)