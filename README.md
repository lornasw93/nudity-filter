# Nudity Filter

#CommandoSquad

Part of the Global Hackathon 2021, a team of volunteers came together to work on a Nudity Filter project. The Monitor/Moderation teams have to deal with very sensitive information. Identifying screenshots for moderation which contains nudity is a legal requirement to protect those having to review such images. The aim is to ultimately blur out NSFW images before the moderation team sees it so 1) they don't see the raw image and 2) only blurred is saved.

I cloned the [NudeNet](https://github.com/notAI-tech/NudeNet) repo and after making progress i.e. successfully blurring images, I gutted the project to the bone so only have what we're using in there - previously was a lot of noise. I had numerous weird issues trying to get the original project up and running - mainly pertaining to packages, but got there.

Changes to original code:

- (Renamed project after changes to nudity-filter)
- Blur instead of black rectangles
- By folder instead of per single file
- Result classes are exported as a JSON file (per flagged image)

Also to note:

- There have been some images that have been blurred when they shouldn't have and vice versa. I'd est. ~80% are correct (by manually checking results)

## Example

This is an example to show what your results could look like when running the below command

```
py detector.py
```

### Before
Check for the file within /example/nude01.jpg

### After
After running the above command, these are the results.

#### JSON File
File contents (within /example/flagged_nude01.json)

```
[
    {
        "box": [ 76, 125, 151, 203 ],
        "score": 0.847710371017456,
        "label": "FACE_F"
    },
    {
        "box": [ 146, 218, 187, 253 ],
        "score": 0.8441938161849976,
        "label": "EXPOSED_ARMPITS"
    },
    {
        "box": [ 240, 363, 377, 497 ],
        "score": 0.8047983646392822,
        "label": "EXPOSED_BUTTOCKS"
    },
    {
        "box": [ 65, 251, 127, 327 ],
        "score": 0.7035146355628967,
        "label": "EXPOSED_BREAST_F"
    }
]
```

#### Image

![After blur effect has been applied on NSFW image](/example/blurred_nude01.jpg)

## Prerequisites

I installed [Python 3.7.9](https://www.python.org/downloads/release/python-379/) specifically (Windows x86-64) as had numerous errors when attempting to run another similar program whilst using the skikit-image package. Most sites recommended downgrading to 3.7. This fixed whatever it was. Also ensure you select true the "Install PATH?" checkbox on the first step of wizard.

I used [anaconda3](https://www.anaconda.com/products/individual) cmd line

## 🏃‍♀️ How to run
Presuming you've cloned the project, check that you're in the correct directory

```
cd C:\repos\nudity-filter
```

To then install required packages

```
py -m pip install -r requirements.txt
```

And head into

```
cd src
```

Where you can now run your commands i.e. 

See 1st example to see `py detector.py` in 🎥 action. This command does the following: (high-level overview)

1. Loop through all images within a specific folder location ("Test Images") on your local drive
2. If NSFW image, a JSON file is generated (in "Results") which contains coordinates of area to blur, scoring and label
3. Image is duplicated with blurring effect on top where appropriate and then saved in a "Results" folder

```
python detector.py
```

!!!!This command isn't working yet!!!! [WIP]

```
python classifier.py
```

## 👨‍🏫 Classes

The class data per image is exported to a single JSON file.

_This is lifted from the original repo, copied here for ease._

### Classifier

| Class  |  Description   |
| ------ | :----------------------------------: |
| safe   | Image/Video is not sexually explicit |
| unsafe |   Image/Video is sexually explicit   |

### Default Detector

| Class    |       Description       |
| ------------------- | :-------------------------------------------: |
| EXPOSED_ANUS        |           Exposed Anus; Any gender |
| EXPOSED_ARMPITS     |          Exposed Armpits; Any gender          |
| COVERED_BELLY       |  Provocative, but covered Belly; Any gender   |
| EXPOSED_BELLY       |           Exposed Belly; Any gender           |
| COVERED_BUTTOCKS    | Provocative, but covered Buttocks; Any gender |
| EXPOSED_BUTTOCKS    |         Exposed Buttocks; Any gender          |
| FACE_F   |       Female Face       |
| FACE_M   |        Male Face        |
| COVERED_FEET        |           Covered Feet; Any gender |
| EXPOSED_FEET        |           Exposed Feet; Any gender |
| COVERED_BREAST_F    |    Provocative, but covered Breast; Female    |
| EXPOSED_BREAST_F    | Exposed Breast; Female  |
| COVERED_GENITALIA_F |  Provocative, but covered Genitalia; Female   |
| EXPOSED_GENITALIA_F |           Exposed Genitalia; Female           |
| EXPOSED_BREAST_M    |  Exposed Breast; Male   |
| EXPOSED_GENITALIA_M | Exposed Genitalia; Male |

### Base Detector

| Class    |         Description          |
| ------------------- | :--------------------------: |
| EXPOSED_BELLY       |  Exposed Belly; Any gender   |
| EXPOSED_BUTTOCKS    | Exposed Buttocks; Any gender |
| EXPOSED_BREAST_F    |    Exposed Breast; Female    |
| EXPOSED_GENITALIA_F |  Exposed Genitalia; Female   |
| EXPOSED_GENITALIA_M |   Exposed Genitalia; Male    |
| EXPOSED_BREAST_M    |     Exposed Breast; Male     |

## 👀 Notes

- If see 'None' in cmd line, means cv2.imread() file was unable to be opened
- The onnxruntime package takes a while to install
