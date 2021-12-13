#include <string>
#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

// Chronological starttimes
//enum startTime{NULLTIME, M800, M905, M1025, M1145, M1250, M155, M315, M435, T800, T930, T1145, T1250, T220, T350};

// Preferred starttimes
enum startTime{NULLTIME, M1250, T1250, M1145, T1145, M1025, T930, M905, M155, T220, M315, T350, M435, T800, M800};
                               
class Class{ //NODE
    public:
        string name, id, prof;
        startTime t;
        vector<Class*> neighbors; // Things connected by edges
        
        Class() : Class("", "", "", NULLTIME){}
        Class(string name) : Class(name, "", "", NULLTIME){}
        Class(string name, string id) : Class(name, id, "", NULLTIME){}
        Class(string name, string id, string prof) : Class(name, id, prof, NULLTIME){}
        Class(string name, string id, string prof, startTime t){
            this->prof=prof;
            this->name=name;
            this->id = id;
            this->t=t;
        }
        
        // Set timeslot for current 
        void setT(startTime t){
            this -> t = t;
        }

        // Add edges between two classes if it doesn't already exist.
        void addNeighbor(Class *c){
            bool has = false;
            for(int i = 0; i < neighbors.size(); i++){
                if(neighbors[i] == c){
                    has = true;
                }
            }
            
            if(!has){
                neighbors.push_back(c);
                c->addNeighbor(this);
            }
        }
        
        void printC(){
            cout << name << ": " << t << ": " << prof;
        }

        void color(){
            //https://iq.opengenus.org/graph-colouring-greedy-algorithm/
            // Consider the currently picked vertex
            // Colour it with the lowest numbered colour
            // that has not been used on any previously colored vertices
            // adjacent to it

            // Set all times/colors to available then go through neighbors and check times and set all neighbor times to unavailable
            vector<bool> availableTimes; 
            for(int i = 0; i < 14; i++){
                availableTimes.push_back(true);
            }

            // For each neighbor mark color as taken
            for(int i = 0; i < neighbors.size(); i++){
                if (neighbors[i]->t != NULLTIME){
                    availableTimes[neighbors[i]->t - 1] = false;
                }
            }
            
            startTime n = NULLTIME;

            for(int i = 0; i < 14; i++){
                if(availableTimes[i]){
                    n = (startTime)(i+1);
                    break;
                }
            }
            if(n == NULLTIME){
                cout << "CANNOT BE COLORED\n";
            } else {
                setT(n);
            }

        }
};

class graph{
    int nodeCount, edgeCount;
    vector<Class*> classes;

    public:
        graph(int nc){
            nodeCount = nc;
        }

        void addClass(Class* a){
            classes.push_back(a);
        }

        void color(){
            //https://iq.opengenus.org/graph-colouring-greedy-algorithm/
            //Do following for remaining V-1 vertices
            // Consider the currently picked vertex
            // Colour it with the lowest numbered colour
            // that has not been used on any previously colored vertices
            // adjacent to it

            // If all previously used colors appear on vertices adjacent to v, assign a new color to it.

            // Start our process with an initial assignment. All others are defaulted to NULLTIME
            classes[0]->setT(M1250);
            for (int i = 1; i < nodeCount; i++){
                classes[i]->color();
            }
        }

        // n^2 edge creation between classes with identical professors
        void neighborProfessors(){
            for(int i = 0; i < classes.size(); i++){
                for(int j = 0; j < classes.size(); j++){
                    if(classes[i]->prof == classes[j]->prof && j != i){
                        classes[i]->addNeighbor(classes[j]);
                    }
                }
            }
        }

        // Print statements for debugging and results output

        void print(){
            for(int i = 0; i < nodeCount; i++){
                cout << i+1 << ": "; classes[i]->printC(); cout << endl;
            }
        }

        void printEdgeCount(){
            int sum =0;
            for(int i = 0; i < nodeCount; i++){
                sum += classes[i]->neighbors.size();
            }

            cout << "EdgeCount: " << sum/2 << endl;
        }
};

int main(){
    vector<Class> classes;
    ifstream fin("input.txt");
    ifstream clin("classInfo.txt");
    int nc, first = 0, second = 1;
    fin >> nc; classes.resize(nc);

    // Fill class information
    for(int i = 0; i < nc; i++){
        clin >> classes[i].id;
        clin >> classes[i].name;
        clin >> classes[i].prof;
    }

    // Normal edge input
    fin >> first >> second;
    while(first != 0 || second != 0){
        classes[first-1].addNeighbor(&classes[second-1]);
        fin >> first >> second;
    }

    graph g(nc);
    for(int i = 0; i < nc; i++){
        g.addClass(&classes[i]);
    }

    g.neighborProfessors();
    g.color();
    g.print();
}
