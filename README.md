# LCD-Digit-Recognition

This project is written in Python. To run this project please make sure you have [Python](https://www.python.org/downloads/ "Python") installed on your machine.

This is a Python program I wrote using [OpenCV](https://opencv.org/ "OpenCV"). It's very small and calibrated to work with this specific display. ([See the data](https://github.com/avigael/LCD-Digit-Recognition/tree/master/data "Data Folder")) The program was trained with 100 images of different numbers on the display which I manually labeled. The reason so many training imaged were used was because the program would scan running off a non-static camera and it was important that numbers collected were accurate.

#### Input

![Program Input](https://github.com/avigael/LCD-Digit-Recognition/blob/master/screenshots/input.png)

#### Output

![Program Output](https://github.com/avigael/LCD-Digit-Recognition/blob/master/screenshots/output.png)

### More Information

We needed to collect a large number of IDs stored on RFID chips very quickly. There was a device which could tell you the ID stored on the RFID tag, but manufacturer restrictions made it impossible to get any of the data off of the device. The only way to get the ID off the RFID was to read the physical number printed on the tag itself. This was a simple yet tedious task, so I knew computer vision would be a great solution to this problem. I wrote the code in a day and made improvements on the fly. RFID tags were stored in CSV files and we managed to cycle through over 500,000 tags.

### Note

I used this program to get a specific set of numbers from the second line on the LCD display. The area used by the program can be adjusted on line 46 `if h > 75 and y > 180 and y < 280:`
```python
 45    # restrict size of digit and placement of digits
 46    if h > 75 and y > 180 and y < 280:
```
