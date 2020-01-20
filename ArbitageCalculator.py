import csv

class ArbitageCalculator:
    def lets_go(self):
        sportsbet_names = []
        sportsbet_overOdds = []
        sportsbet_underOdds = []
        sportsbet_points = []

        with open('sportsbet_Odds.csv') as csv_file :

            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                sportsbet_names.append(row[0][:row[0].find("-")-1] + row[0][row[0].find("|"):])
                sportsbet_overOdds.append(row[1])
                sportsbet_underOdds.append(row[2])
                sportsbet_points.append(row[3][row[3].find("+")+1:-1])

        bet365_names = []
        bet365_overOdds = []
        bet365_underOdds = []
        bet365_points = []

        with open('bet365_Odds.csv') as csv_file :

            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                # if(len(row)==1):
                #     game_name = row[0] 
                #     continue
                bet365_names.append(row[0])
                bet365_overOdds.append(row[1])
                bet365_underOdds.append(row[2])
                bet365_points.append(row[3])


        best_over = 0.0;
        best_under = 0.0;
        games_found = 0;
        arbitages_found = 0;
        points_diff = 0;
        not_arbitage = 0;

        i = 0
        while(i < len(sportsbet_names)) :
            j = 0
            while(j < len(bet365_names)) :
                if (sportsbet_names[i] == bet365_names[j]) :
                    games_found+=1
                    if sportsbet_points[i] != bet365_points[j] :
                        points_diff+=1
                        j+=1
                        continue

                    if sportsbet_overOdds[i] > bet365_overOdds[j] :
                        best_over = sportsbet_overOdds[i]
                        best_under = bet365_underOdds[j]
                    else:
                        best_over = bet365_overOdds[j]
                        best_under = sportsbet_underOdds[i]
                    
                    # Arbitage formula -> https://youtu.be/TGinzvSDayU?t=333 
                    calc = (1/float(best_over) + 1/float(best_under)) * 100;

                    if (calc < 100) :
                        # print(game_name)
                        print("################################") 
                        print("ARBITAGE FOUND!!! -> " , sportsbet_names[i]) 
                        print("Profit margin of -> " , round(100-calc,3))

                        print("\nSportsbet Over " , sportsbet_overOdds[i]) 
                        print("Sportsbet Under " , sportsbet_underOdds[i])

                        print("\nBet365 Over " , bet365_overOdds[j])
                        print("Bet365 Under " , bet365_underOdds[j])

                        print("\nBest Over " , best_over )
                        print("Best Under " , best_under)
                        print("################################") 
                        arbitages_found+=1;
                    else:
                        not_arbitage+=1;
                j+=1
            i+=1

        print("\nPotential arbitages:" , games_found)
        print("Arbitages found:" , arbitages_found)
        print("Games with different points:" , points_diff)
        print("Not arbitages:" , not_arbitage)