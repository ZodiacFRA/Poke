//Uncomment the following line if you are compiling this code in Visual Studio
//#include "stdafx.h"

#include <cassert>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <string>

using namespace cv;
using namespace std;

long getTime(){
    return std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
}



// std::vector<std::vector<std::vector<char>>>  decoded_map;
std::map<int,std::map<int,int>>   id_map;
std::vector<std::vector<int>>   ref_table;
int                             sprite_size = 16;

int                             map_width;
Mat image;


bool compare_img(int x, int y, int i, int j) {
    for (int a = 0; a < sprite_size; ++a) {
        for (int b = 0; b < sprite_size; ++b) {
            if (image.at<Vec3b>(cv::Point(x + a, y + b)) != image.at<Vec3b>(cv::Point(i + a, j + b))) {
                return false;
            }
        }
    }
    return true;
}

void draw_image(int x , int y, int num, int xa , int ya) {
    if (y == 6400)
        return;
    // String windowName = "The Guitar " + std::to_string(x) + " " + std::to_string(y); //Name of the window
    String windowName = "The Guitar " + std::to_string(num); //Name of the window

    namedWindow(windowName); // Create a window
    // cv::Rect myROI(x,y,32,32);
    cv::Rect myROI(x,y,sprite_size,sprite_size);
    cv::Rect myROI2(xa,ya,16,16);
    auto crop = image(myROI);
    auto crop2 = image(myROI2);


    cv::imwrite("data/" + std::to_string(num) + ".png", crop);

    imshow(windowName, crop); // Show our image inside the created window.
    //waitKey(0); // Wait for any keystroke in the windowll
    // imshow(windowName, crop2); // Show our image inside the created window.

    // waitKey(0); // Wait for any keystroke in the window

    destroyWindow(windowName); //destroy the created window
}

bool compare_tile_to_refs(int x, int y) {
    int a = 0;
    for (auto ref : ref_table) {
        if (compare_img(x, y, ref[0], ref[1])) {
            id_map[y/sprite_size][x/sprite_size] = a;
            return true;
        }
        ++a;
    }
    id_map[y/sprite_size][x/sprite_size] = ref_table.size();
    return false;
}

void save_map_to_json(std::string path) {
    ofstream myfile;
    myfile.open (path);
    myfile << "{\"map\": [\n";
    for (int y = 0; y < id_map.size() - 1; ++y) {
        myfile << "[";
        for (int x = 0; x < id_map.size(); ++x) {
            myfile << std::right << std::setw(5) << id_map[x][y] << ",";
        }
        myfile << std::right << std::setw(5) << id_map[id_map.size()-1][y] << "],\n";

    }
    myfile << "],\n\"ref\":{";
    for (int x = 0; x < ref_table.size() - 1; ++x) {
            myfile << "\"" << x << "\": [" << ref_table[x][0] << ", " << ref_table[x][1] << "],\n";
            std::cout << ref_table[x][0] << ", " << ref_table[x][1] <<std::endl;
            draw_image(ref_table[x][0],ref_table[x][1],x,0,0);
    }
    myfile << "\"" << ref_table.size() - 1 << "\": [" << ref_table[ref_table.size() - 1][0] << ", " << ref_table[ref_table.size() - 1][1] << "],\n";
    myfile << "}}";
    myfile.close();

    std::cout << "final size: " << ref_table.size() << std::endl;
}

int main(int argc, char** argv)
{
    // Read the image file
    image = imread("/home/seub/Downloads/mathieugrosfdp.png");

    auto size = image.size();
    std::cout << size.height << " " << size.width << std::endl;

    for (int y = 0; y < size.height - sprite_size/2; y += sprite_size) {
        for (int x = 0; x < size.width - sprite_size/2; x += sprite_size) {
            bool exist = compare_tile_to_refs(x,y);
            if (!exist) {
                ref_table.push_back({x,y});
                std::cout << "add ref: " << x << ":" << y << std::endl;
            }
        }
    }

    save_map_to_json("map_out.json");

    return 0;
}