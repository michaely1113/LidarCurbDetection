## Welcome

Curb Detection Using Hough Transform on Lidar Data

I've included sample data in `/sample`.

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