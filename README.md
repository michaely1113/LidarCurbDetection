## Welcome

Curb Detection Using Hough Transform on Lidar Data

I've included sample data in `/sample`. I've not been able to include Lidar data
because of the Lidar file size/Github file size limit. See the section below `Data` to
see how to gather Lidar data.

### Getting Lidar Data
1. Register and make account here:
http://pugetsoundlidar.ess.washington.edu/lidardata/account.php

2. Data is here: download any one of the *.laz files
 http://pugetsoundlidar.ess.washington.edu/lidardata/restricted/las/pslc2016/KingCounty_Delivery_1/

.laz is compressed version of .las. You usually work with .las. Here’s how to go from .laz to .las:

3. Download this: https://rapidlasso.com/LAStools/

4. Go into that folder, then from there, in terminal, run ‘make’. 

5. Then, go into /bin, then run the executable `laszip`. It should open up a terminal: you can input a file path, and an output file path (.laz to .las)

6. To visualize, here is a site that’s simple: http://lidarview.com/



### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/michaely1113/LidarCurbDetection.git
  $ cd LidarCurbDetection
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv -p python3 env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

5. Run the main code:
  ```
  $ python main.py
  ```
  
### Note

After the .jpg files are generated, you may need to manually crop them to remove the white space
in order for the hough transform algorithms to work accurately.