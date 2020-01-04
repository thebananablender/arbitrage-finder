#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

int main(int argc, char const *argv[])
{
	ifstream file1("sportsbet_Odds.csv");
	vector<string> names;

	string game;
	string name1;
	string over_Odd1;
	string under_Odd1;
	string point1;

	vector<string> names1;
	vector<double> over_Odds1;
	vector<double> under_Odds1;
	vector<double> points1;

	// Extracting odds from sportsbet_Odds.csv
	while(file1.good())
	{
		getline(file1,name1,',');
		getline(file1,over_Odd1,',');
		getline(file1,under_Odd1,',');
		getline(file1,point1,'\n');

		names1.push_back(name1);
		names.push_back(name1);
		over_Odds1.push_back(stod(over_Odd1));
		under_Odds1.push_back(stod(under_Odd1));

		point1 = point1.substr(point1.find("+")+1,point1.find(")")-point1.find("+"));
		points1.push_back(stod(point1));
	}


	// cout << "******Sportsbet Odds******" << endl;
	for (int i = 0; i < names1.size()-1; i++)
	{
		names1[i] = names1[i].erase(names1[i].find("-")-1,names1[i].find("|")-(names1[i].find("-")-1));
		// cout << names1[i] << endl;
	}

	ifstream file2("bet365_Odds.csv");

	getline(file2,game,'\n');

	string name2;
	string over_Odd2;
	string under_Odd2;
	string point2;

	vector<string> names2;
	vector<double> over_Odds2;
	vector<double> under_Odds2;
	vector<double> points2;

	// Extracting odds from bet365_Odds.csv
	while(file2.good())
	{
		getline(file2,name2,',');
		getline(file2,over_Odd2,',');
		getline(file2,under_Odd2,',');
		getline(file2,point2,'\n');

		names2.push_back(name2);
		over_Odds2.push_back(stod(over_Odd2));
		under_Odds2.push_back(stod(under_Odd2));

		points2.push_back(stod(point2));
	}

	double bestOver = 0.0;
	double bestUnder = 0.0;

	// Looking for matching games
	for (int i = 0; i < names1.size()-1; i++)
	{
		for (int j = 0; j < names2.size()-1; j++)
		{
			if (names1[i]==names2[j])
			{
				cout << "################################" << endl; 
				cout << game << endl << endl;
				cout << "Same Game Found: " << names[i] << endl;

				// When games have different points we are not actually betting on the same thing
				// So we skip these.
				if (points1[i]!=points2[j])
				{
					cout << "Points are different :(" << endl << endl;

					cout << "Sportsbet Points " << points1[i] << endl;
					cout << "Bet365 Points " << points2[j] << endl;
					cout << "################################" << endl << endl; 
					continue;
				}

				if(over_Odds1[i]>over_Odds2[j])
				{
					bestOver = over_Odds1[i];
					bestUnder = under_Odds2[j];
				} else {
					bestOver = over_Odds2[j];
					bestUnder = under_Odds1[i];
				}

				//arbitage formula -> https://youtu.be/TGinzvSDayU?t=333 
				const auto calc = (1/bestOver+1/bestUnder)*100;

				if (calc < 100)
				{
					cout << "ARBITAGE FOUND!!! -> " << names[i] << endl << endl; 
					cout << "Profit margin of -> " << 100-calc << endl << endl; 

					cout << "Sportsbet Over " << over_Odds1[i] << endl;
					cout << "Sportsbet Under " << under_Odds1[i] << endl << endl;

					cout << "Bet365 Over " << over_Odds2[j] << endl;
					cout << "Bet365 Under " << under_Odds2[j] << endl << endl;

					cout << "Best Over " << bestOver << endl; 
					cout << "Best Under " << bestUnder << endl ; 
				} else {
					cout << "not an arbitage :(" << endl;
				}
				cout << "################################" << endl << endl; 
			}
		}
	}


	return 0;
}