//This program returns the moving average over the last r years of a time series dataset
//Please use input files composed of 2 columns: the first containing the year (must be an integer),
//the second containing the relative data (double). Please don't leave comments, extra columns, 
//invalid types or anything but the specified 2 cols with only the data. There's no error checking.
//Use tabs as separators (spaces should work fine tho).
//Usage: $./moving_avg <filename.txt> <refinement (int)> > output.dat
//Made by Lorenzo Ramella lorenzo.ramella@studenti.unimi.it 

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <iterator>
#include <numeric>

struct datapoint{
	long year;
	double dat;
	double avg;
};

int main(int argc, char** argv)
{

	long r;
	std::string refinement;
	std::string file_name;

	if(argc < 3) {
		std::cout << "Program usage: <file_name> <resolution>" << std::endl;
		std::cout << "Type in the name of the file you want to use: ";
		std::cin >> file_name;
		std::cout << "\nType in the refinement of your moving average (must be an integer): ";
		std::cin >> r;
		std::cout << std::endl;
	}
	else{
		file_name = argv[1];
		refinement = argv[2];
		r = std::stol(refinement);
	}
	std::ifstream in(file_name);

	if(!in) { // checks for errors while opening file
		std::error_code err_code(errno, std::system_category());
		std::cerr << "Error opening \"" << file_name << "\" with error: " 
				<< err_code.message() << std::endl;
	return 2;
	}

	std::vector<datapoint> v;
	while(in.good()) {
		datapoint slave;
		in>>slave.year>>slave.dat;
		v.push_back(slave);
	}

	long year0 = v[0].year;
	for (auto i : v) if (i.year < year0) year0 = i.year;

	//for (auto i : v) std::cout<<i.year<<"\t"<<i.dat<<std::endl; //debug
	bool whoops = false;
	for (auto &i : v){
		double a = 0;
		int count = 0;
		for (auto j : v){
			if (j.year <= i.year && j.year > i.year - r) { a += j.dat; ++count; }
		}
		if (count!=0) i.avg = a/count;
		else {i.avg = 0; if (i.year != year0) whoops=true;}
	}

	for (auto i : v) if (i.year >= year0 + r) std::cout<<i.year<<"\t"<<i.dat<<"\t"<<i.avg<<std::endl;	
	if(whoops == true) std::cout<<"There might be a problem with the refinement. It might be too small. You might want to increase it."<<std::endl;

	return 0;
}
