//Uncomment the following line if you are compiling this code in Visual Studio
//#include "stdafx.h"

#include <cassert>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

long getTime(){
    return std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
}



// std::vector<std::vector<std::vector<char>>>  decoded_map;
std::vector<std::vector<int>>   id_map;
std::vector<std::vector<int>>   ref_table;
int                             sprite_size = 16;

int                             map_width;
Mat image;


bool compare_img(int x, int y, int i, int j) {
    // std::cout << "heinnnnnnnn" << (void*)img1 << " " << (void*)img2 << std::endl;
    for (int i = 0; i < sprite_size; ++i) {
        for (int j = 0; j < sprite_size; ++j) {
            if (image.at<Vec3b>(x, y) != image.at<Vec3b>(i, j)) {
                auto a = image.at<Vec3b>(x, y);
                auto b = image.at<Vec3b>(i, j);
                std::cout << (int)a[0] - (int)b[0] << " " << (int)a[1] - (int)b[1] << " " << (int)a[2] - (int)b[2] << std::endl;
                return false;
            }
        }
    }
    return true;
}

void draw_image(int x , int y, int num, int xa , int ya) {
    // String windowName = "The Guitar " + std::to_string(x) + " " + std::to_string(y); //Name of the window
    String windowName = "The Guitar " + std::to_string(num); //Name of the window

    namedWindow(windowName); // Create a window
    // cv::Rect myROI(x,y,32,32);
    cv::Rect myROI(x,y,100,100);
    cv::Rect myROI2(xa,ya,16,16);
    auto crop = image(myROI);
    auto crop2 = image(myROI2);

    imshow(windowName, crop); // Show our image inside the created window.
    //waitKey(0); // Wait for any keystroke in the windowll
    imshow(windowName, crop2); // Show our image inside the created window.

    //waitKey(0); // Wait for any keystroke in the window

    destroyWindow(windowName); //destroy the created window
}

bool compare_tile_to_refs(int x, int y) {
    for (auto ref : ref_table) {
        if (compare_img(x, y, ref[0], ref[1]))
            return true;
    }
    return false;
}

int main(int argc, char** argv)
{
    // Read the image file
    image = imread("/home/seub/Downloads/mathieugrosfdp.png");

    auto size = image.size();
    map_width = size.width * 3;

    // decoded_map.resize(size.width + 100);
    id_map.resize((size.width / sprite_size) + 100);
    for (int x = 0; x < size.height/sprite_size; ++x) {
        id_map[x].reserve((size.height / sprite_size) + 100);
        // decoded_map[x].resize(size.height + 100);
        for (int y = 0; y < size.width/sprite_size; ++y) {
            std::cout << x << ":" << y << std::endl;
            // auto const &tmp = image.at<Vec3b>(x, y);
            // decoded_map[x][y].push_back(tmp[0]);
            // decoded_map[x][y].push_back(tmp[1]);
            // decoded_map[x][y].push_back(tmp[2]);
            id_map[x].emplace_back(0);
        }
    }

    assert(compare_img(0,160,0,160) == true);
    assert(compare_img(0,160,sprite_size*2,160) == true);
    assert(compare_img(0,0,0,160) == false);

    std::cout << "poutis" << std::endl;
    auto before = getTime();
    int tf = 0;
    for (int y = 0; y < size.height; y += sprite_size) {

        for (int x = 0; x < size.width; x += sprite_size) {
            ++tf;
            bool exist = compare_tile_to_refs(x,y);
            if (!exist)
                ref_table.push_back({x,y});
        }
        auto after_y_iter = getTime();
        if (y)
        std::cout << "stat: " << ref_table.size() << "/" << tf << std::endl;// << ((after_y_iter - before)/ y) * (size.height-y) << std::endl;
    }

    for (auto elem : ref_table) {
        // std::cout << "ref " << elem[0] << ":" << elem[1] << std::endl;
    }

    std::cout << tf << std::endl;
    std::cout << "final size: " << ref_table.size() << std::endl;


    return 0;
}