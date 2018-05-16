# CSV-to-HTML-for-psychologists
converts .csv file to .html file for psychological experiments

# Usage:
    python3 generate_html.py <instruction>.txt <experiment>.csv

# CSV(utf-8) template
Note that the name of first row can be changed

response(b/k): b if button, k if keyboard<br>
content: path to the image or text<br>
content-type: image/text<br>
choices(space_split): space-splitted contents<br>
choice_type: image/text<br>
duration(ms): if time is elapsed beyond duration, continue the exp<br>
correct(0~): the answer<br>
unit_type: trial/test/fix/result<br>
feedback: y/n<br>
feedback_type: image/text<br>
true_content: show the content if true<br>
false_content: show the content if true<br>
feedback_duration(ms)<br>
