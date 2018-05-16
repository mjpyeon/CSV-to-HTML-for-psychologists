##### CSV-to-HTML-for-psychologists
###converts .csv file to .html file

#### Usage:
    python generate_html.py <instruction>.txt <experiment>.csv

#### CSV(utf-8) template:
## Note that the name of first row can be changed
# response(b/k): b if button, k if keyboard	
# content: path to the image or text
# content-type: image/text
# choices(space_split): space-splitted contents
# choice_type: image/text	
# duration(ms): if time is elapsed beyond duration, continue the exp
# correct(0~): the answer
# unit_type: trial/test/fix/result
# feedback: y/n
# feedback_type: image/text	
# true_content: show the content if true
# false_content: show the content if true
# feedback_duration(ms)
