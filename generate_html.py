"""
Generate HTML files for psychological experiments
Requirement: 
    argv[1]: <instruction>.txt
    argv[2]: <experiment>.csv
CSV(utf-8) template:
    < Note that the name of first row can be changed>
    response(b/k): b if button, k if keyboard	
    content: path to the image or text
    content-type: image/text
    choices(space_split): space-splitted contents
    choice_type: image/text	
    duration(ms): if time is elapsed beyond duration, continue the exp
    correct(0~): the answer
    unit_type: trial/test/fix/result
    feedback: y/n
    feedback_type: image/text	
    true_content: show the content if true
    false_content: show the content if true
    feedback_duration(ms)
Output:
    (<experiment>_inst.html, <experiment>.html)
"""
# -*- coding: utf-8 -*-
import sys


class Unit():
    def __init__(self, response, content, content_type,	\
                choices=None, choice_type=None,	duration=None,	correct=None, unit_type=None,	\
                feedback=None,	feedback_type=None,	true_content=None, false_content=None, feedback_duration=None):
        self.response = response
        self.content_type = content_type
        self.content = content
        self.choice_type = choice_type
        self.choices = choices.split(" ")
        #print(self.choices)
        self.duration = duration
        self.correct = correct
        self.unit_type = unit_type
        if feedback=="y":
            self.feedback=True
        else:
            self.feedback=False
        self.feedback_type = feedback_type
        self.true_content = true_content
        self.false_content = false_content
        self.feedback_duration = feedback_duration


    def get_response_string(self):
        if self.response == "b":
            return "\'html-button-response\'"
        elif self.response == "k":
            return "\'html-keyboard-response\'"
        else:
            print("ERROR: Wrong Response Type")
            sys.exit(0)
    
    def get_stimulus_string(self):
        if self.content_type == "image":
            return "\'<img src = \""+ self.content +"\"><br><br>\'"
        elif self.content_type == "text":
            return "\"" + self.content + "\""
        elif self.unit_type == "result":
            return "function () {\n\
				var trials = jsPsych.data.get().filter({ test_part: \'test\' });\n\
				var correct_trials = trials.filter({ correct: true });\n\
				var accuracy = Math.round(correct_trials.count() / trials.count() * 100);\n\
				var rt = trials.select(\'rt\').values;\n\
				return \"<p>You responded correctly on \" + accuracy + \"% of the trials.</p>\" +\n\
					\"<p>Your average response time was \" + rt + \"ms.</p>\" +\n\
					\"<p>Press any key to complete the experiment. Thank you!</p>\";\n\
			}"
        else:
            print("ERROR: Wrong Stimulus Type")
            sys.exit(0)
    
    def get_choice_string(self):
        if self.unit_type == "result":
            return None
        elif self.unit_type == "fix":
            return "jsPsych.NO_KEYS"
        elif len(self.choices) == 1 and self.choices[0]=='':
            return None
        return_string = "["
        if self.choice_type == "image":
            for choice in self.choices:
                return_string += "\'<img src=\""+ choice +"\">\',"
            return_string = return_string[:-1]
            return_string += "]"
        elif self.choice_type == "text":
            for choice in self.choices:
                return_string += "\"" + choice + "\","
            return_string = return_string[:-1]
            return_string += "]"
        return return_string
    
    def get_data_string(self):
        if self.unit_type == "result":
            return None
        elif self.correct == '':
            return "{ test_part: \"" + self.unit_type +"\"}"
        else:
            return "{ test_part: \"" + self.unit_type +"\", correct_response: " + self.correct + "}"

    def get_trial_duration_string(self):
        if self.duration == "":
            return None
        else:
            return self.duration

    def get_on_finish_string(self):
        if self.unit_type == "result" or self.unit_type == "fix":
            return None
        else:
            return "function (data) {\n\
                    data.correct = data.button_pressed == data.correct_response;\n\
                    }"

    def get_feedback_correct_string(self):
        #print(self.feedback_duration)
        if not self.feedback:
            return None
        elif self.feedback_type == "image":
            if self.feedback_duration == "":
                return "{\n\
                    type: \'html-keyboard-response\',\n\
                    stimulus: \'<img src=\"%s\">\'\n\
                    }"%(self.true_content)
            else:
                return "{\n\
                    type: \'html-keyboard-response\',\n\
                    stimulus: \'<img src=\"%s\">\',\n\
                    trial_duration: %s\n\
                    }"%(self.true_content, self.feedback_duration)
        elif self.feedback_type == "text":
            if self.feedback_duration == "":
                return "{\n\
                    type: \'html-keyboard-response\',\n\
                    stimulus: \'%s\'\n\
                    }"%(self.true_content)
            else:
                return "{\n\
                    type: \'html-keyboard-response\',\n\
                    stimulus: \'%s\',\n\
                    trial_duration: %s\n\
                    }"%(self.true_content, self.feedback_duration) 
        else:
            print("ERROR: Wrong feedback type")
            sys.exit()

    def get_feedback_wrong_string(self):
        if not self.feedback:
            return None
        elif self.feedback_type == "image":
            if self.feedback_duration == "":
                return "{\n\
                    type: \'html-keyboard-response\',\n\
                    stimulus: \'<img src=\"%s\">\'\n\
                    }"%(self.false_content)
            else:
                return "{\n\
                    type: \'html-keyboard-response\',\n\
                    stimulus: \'<img src=\"%s\">\',\n\
                    trial_duration: %s\n\
                    }"%(self.false_content, self.feedback_duration)
        elif self.feedback_type == "text":
            if self.feedback_duration == "":
                return "{\n\
                    type: \'html-keyboard-response\',\n\
                    stimulus: \'%s\'\n\
                    }"%(self.false_content)
            else:
                return "{\n\
                    type: \'html-keyboard-response\',\n\
                    stimulus: \'%s\',\n\
                    trial_duration: %s\n\
                    }"%(self.false_content, self.feedback_duration) 
        else:
            print("ERROR: Wrong feedback type")
            sys.exit()

    def get_feedback_block(self):
        corr_block =  "timeline.push({\n\
					timeline: [%s],\n\
					conditional_function: function (data) {\n\
						var data = jsPsych.data.get().last(1).values()[0];\n\
						if (data.correct_response == data.button_pressed) {\n\
							return true;\n\
						} else {\n\
							return false;\n\
						}\n\
					}\n\
				});"%(self.get_feedback_correct_string())
        wrong_block = "timeline.push({\n\
					timeline: [%s],\n\
					conditional_function: function (data) {\n\
						var data = jsPsych.data.get().last(1).values()[0];\n\
						if (data.correct_response == data.button_pressed) {\n\
							return false;\n\
						} else {\n\
							return true;\n\
						}\n\
					}\n\
				});"%(self.get_feedback_wrong_string())
        return corr_block + "\n" + wrong_block
    
    def get_experiment_block(self):
        return_str = "timeline.push({\n"
        return_str += "type: " + self.get_response_string() + ",\n"
        return_str += "stimulus: " + self.get_stimulus_string() + ",\n"
        trial_duration = self.get_trial_duration_string()
        if trial_duration is not None:
            return_str += "trial_duration: " + trial_duration + ",\n"
        choices = self.get_choice_string()
        if choices is not None:
            return_str += "choices: " + choices + ",\n"
        data = self.get_data_string()
        if data is not None:
            return_str += "data: " + data + ",\n"
        if self.unit_type == "trial" or self.unit_type == "test":
            return_str += "response_ends_trial: true,\n"
        on_finish = self.get_on_finish_string()
        if on_finish is not None:
            return_str += "on_finish :" + on_finish + "\n"
        return_str += "});"
        return return_str
    
    def get_block(self):
        if self.feedback:
            return self.get_experiment_block() + "\n" + self.get_feedback_block() 
        else:
            return self.get_experiment_block()

def get_header(exp_name):    
    return "<head>\n\
        <title>%s</title>\n\
        <meta charset=\"utf-8\">\n\
        <script src=\"jspsych.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-html-keyboard-response.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-html-button-response.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-fullscreen.js\"></script>\n\
        <script src=\"jspsych-6/plugins/jspsych-categorize-html.js\"></script>\n\
        <link rel=\"stylesheet\" href=\"jspsych.css\"></link>\n\
        <script src=\"https://code.jquery.com/jquery-3.3.1.min.js\" integrity=\"sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=\"\n\
        crossorigin=\"anonymous\"></script>\n\
        </head>"%(exp_name)

def get_body(fname):
    body_string = "<body>\n<script>\n"
    body_string += "var timeline = [];\n"
    with open(fname, "r", encoding='utf-8') as f:
        lines = f.readlines()
        line_length = len(lines[0].split(','))
        for line in lines[1:]:
            line = line.replace("\n","").split(',')
            if line_length == len(line):
                unit = Unit(*line)
                body_string += unit.get_block() + '\n'
    body_string += 	"jsPsych.init({\n\
			timeline: timeline,\n\
			show_preload_progress_bar: true,\n\
            on_finish: function() {\n\
                jsPsych.data.get().localSave('csv','data.csv');\n\
            }\n\
		});\n"
    body_string += "</script>\n</body>"
    return body_string

    
            
if __name__ == "__main__":
    """
    Generate "<instruction>.html"
    """
    f_inst = open(sys.argv[1], "r", encoding="utf-8")
    instruction_list = f_inst.readlines()
    f_inst.close()
    instruction_text = ""
    for line in instruction_list:
        instruction_text += line
    #print(instruction_text)
    instruction_text = instruction_text.replace("\n", "<br>")
    instruction = "<!DOCTYPE html>\n\
    <html lang=\"en\">\n\
    <head>\n\
        <meta charset=\"utf-8\">\n\
        <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n\
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n\
    \n\
        <title>" + sys.argv[2].replace('.csv','') + "</title>\n\
    \n\
        <meta name=\"description\" content=\"Source code generated using layoutit.com\">\n\
        <meta name=\"author\" content=\"LayoutIt!\">\n\
    \n\
    <link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css\" integrity=\"sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4\" crossorigin=\"anonymous\">\n\
    \n\
    </head>\n\
    <body>\n\
    \n\
        <div class=\"container-fluid\">\n\
        <div class=\"row\">\n\
            <div class=\"col-md-12\">\n\
                <div class=\"jumbotron\" style=\"text-align: center\">\n\
                    <h2>\n\
                        "+ instruction_text +"\n\
                    </h2>\n</div>\n\
                <div class=\"d-flex justify-content-center\">\n\
                <a role=\"button\" class=\"btn btn-primary btn-lg\" href=\""+ sys.argv[2].replace('.csv','')+'.html' +"\">\n\
                    START\n\
                </a><div>\n\
            </div>\n\
        </div>\n\
    </div>\n\
    \n\
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->\n\
        <script src=\"https://code.jquery.com/jquery-3.3.1.slim.min.js\" integrity=\"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo\" crossorigin=\"anonymous\"></script>\n\
        <script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js\" integrity=\"sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ\" crossorigin=\"anonymous\"></script>\n\
        <script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js\" integrity=\"sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm\" crossorigin=\"anonymous\"></script>\n\
    </body>\n\
    </html>"
    #print(instruction)
    f_inst = open(sys.argv[1].replace('.txt','')+".html", "w+", encoding="utf-8")
    f_inst.write(instruction)
    f_inst.close()

    """
    Generate "<experiment>.html"
    """
    experiment = "<html>\n"
    experiment += get_header(sys.argv[2].replace('.csv','')) + "\n"
    experiment += get_body(sys.argv[2]) + "\n"
    experiment += "</html>"
    f_exp = open(sys.argv[2].replace('.csv','')+'.html', 'w+', encoding="utf-8")
    f_exp.write(experiment)
    f_inst.close()