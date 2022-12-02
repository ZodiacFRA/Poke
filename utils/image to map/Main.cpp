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



std::vector<char>               decoded_map;
std::vector<int>                id_map;
std::vector<std::vector<int>>   ref_table;
int                             sprite_size = 16;

int                             map_width;
Mat image;


bool compare_img(char* img1, char* img2) {
    // std::cout << "heinnnnnnnn" << (void*)img1 << " " << (void*)img2 << std::endl;
    for (int y = 0; y < sprite_size; ++y) {
        for (int x = 0; x < sprite_size; ++x) {
            if (img1[x + 0] - img2[x + 0] > 10)
                return false;
            if (img1[x + 1] - img2[x + 1] > 10)
                return false;
            if (img1[x + 2] - img2[x + 2] > 10)
                return false;
        }
        img1 += map_width;
        img2 += map_width;
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

void main_work(int x, int y) {
    char *ptr_ref_tested = &decoded_map.data()[x*3 + y * map_width];
    std::cout << "start " << x << " " << y << std::endl;
    draw_image(x,y,0,0,0);
    for (int ref_id = 0; ref_id < ref_table.size(); ++ref_id) {
        char *ptr_ref = &decoded_map.data()[ref_table[ref_id][0] * 3 + ref_table[ref_id][1] * map_width];
        draw_image(x,y,ref_id, ref_table[ref_id][0],ref_table[ref_id][1]);
        auto ret = compare_img(ptr_ref_tested, ptr_ref);
        if (ret){
            id_map[(x/sprite_size) + (y/sprite_size)*(map_width/3)] = ref_id;
            return;
        }
    }
    id_map[(x/sprite_size) + (y/sprite_size)*(map_width/3/16)] = ref_table.size();
    ref_table.push_back({x,y});
}

int main(int argc, char** argv)
{
    // Read the image file
    image = imread("/home/seub/Downloads/mathieugrosfdp.png");

    auto size = image.size();
    map_width = size.width * 3;

    decoded_map.reserve(size.height * size.width * 3);
    id_map.reserve((size.width / sprite_size) * (size.height / sprite_size));
    for (int y = 160; y < size.width; ++y) {
        for (int x = 0; x < size.height; ++x) {
            auto const &tmp = image.at<Vec3b>(x, y);
            decoded_map.emplace_back(tmp[0]);
            decoded_map.emplace_back(tmp[1]);
            decoded_map.emplace_back(tmp[2]);
            id_map.emplace_back(0);
        }
    }

    main_work(0, 0);
    main_work(0, 0);
    assert(compare_img(decoded_map.data()+16*sprite_size,decoded_map.data()+16*sprite_size) == true);
    assert(compare_img(decoded_map.data()+16*sprite_size,decoded_map.data()+69*sprite_size) == false);
    assert(ref_table.size() == 1);

    auto before = getTime();
    int tf = 0;
    for (int y = 160; y < size.height; y += sprite_size) {

        for (int x = 0; x < size.width; x += sprite_size) {
            ++tf;
            main_work(x, y);
            std::cout << "ref size: " << ref_table.size() << "/" << tf << std::endl;
            if (ref_table.size() == 10) {
                for(auto elem : ref_table)
                draw_image(elem[0], elem[y], 0,0,0);
            }
        }
        auto after_y_iter = getTime();
        if (y)
        std::cout << "remaining ms: " << ((after_y_iter - before)/ y) * (size.height-y) << std::endl;
    }

    for (auto elem : ref_table) {
        // std::cout << "ref " << elem[0] << ":" << elem[1] << std::endl;
    }

    std::cout << tf << std::endl;
    std::cout << "final size: " << ref_table.size() << std::endl;


    return 0;
}