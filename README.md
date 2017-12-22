# 3D Printer Word Search Solver Using OCR and AI
This software takes as input a picture or image of a word search puzzle and another of the words to look for, solves the puzzle, and generates g-code for a 3D printer such that the printer can solve the puzzle if it has a marker/pen attached to it.

## Required packages
  * tesseract-ocr
  * opencv-python
  * matplotlib
  * numpy

## Instructions
### Extracting Letters

The first thing we want to do to extract the letters is to pre-process our pictures. Ensure that the images are aligned vertically. Crop any words or stray lines that are not necessary. As necessary, run the thresholding and erosion file thresh.py before running tesseract as follows:

`python thresh.py -i pathtoimg`

Once the preprocessing is finished, tesseract needs to be run. The first step is to verify that characters and words are being read correctly. Different [page segmentation methods](https://github.com/tesseract-ocr/tesseract/wiki/ImproveQuality#page-segmentation-method) will lead to different results. Tesseract can be run as follows:

`tesseract pathtoimg -psm N stdout`

Where N is the page segmentation method (see link). I had luck with 6 (Assume a single uniform block of text) for the letters in the puzzle and 11 (Sparse text. Find as much text as possible in no particular order) for the words themselves.

`stdout` prints out the text that it finds. Scroll through and ensure that the letters are in the [appropriate order](http://jeronimomora.com/word-search-cv-cnc/images/tesseract.PNG) and that all words are present. Stray text is fine as it will be ignored by the python code.

Once you have verified that all text is correct, run tesseract again as follows and name your output files. We will place the names of your files in our config file later.

`tesseract pathtoimg -psm N output_filename`
