"""This Module holds the related Functions for writing the Questions to an xml-File

It is planned to rework those Functions, because they're not quite elegant.
"""

from .stringHelpers import get_bullet_string

def write_question_MC(save_dir, ID, name, s_1, s_2, s_3, points_avail, ans_type, true_ans, false_ans, pic):
    """Funktion schreibt MC-Frage auf Grundlage der übergebenen strings nach Pfad f_path"""
    perc = ['100', '50', '33.33333', '25', '20', '16.66667', '14.28571', '12.5', '11.11111', '10']
    num_true = int(len(true_ans))
    perc_true = perc[num_true-1]
    num_false = int(len(false_ans))
    perc_false = '-'+perc_true
    q_name = ID + '_' + name
    f_path = ( save_dir / q_name ).with_suffix('.xml')

    with open(f_path,'w', encoding='utf-8') as f:
    # Text schreiben
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<quiz>\n')
        f.write('<question type="multichoice">\n')
        f.write('<name>\n')
        f.write('<text>' + q_name + '</text>\n')
        f.write('</name>\n')
        f.write('<questiontext format="html">\n')
        if pic != 0:
            f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"> <b>ID ' +str(ID)+ '</b> <br></p>'\
                        '<p dir="ltr" style="text-align: left;">' + s_1 + '<br></p>'\
                            '<p dir="ltr" style="text-align: left;">' + s_2 + '<br></p>'\
                                '<p dir="ltr" style="text-align: left;">' + s_3 + '<br><br></p>'\
                                    '<br><img src="@@PLUGINFILE@@/'+ str(ID) + '.svg" alt="Bild" width="500"><br>'\
                                        '<br></p>]]></text>\n')
            f.write(str(pic))
        else:
            f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"> <b>ID '+q_name+' </b> <br></p>'\
                                    '<p dir="ltr" style="text-align: left;">' + s_1 + '<br></p>'\
                                        '<p dir="ltr" style="text-align: left;">' + s_2 + '<br></p>'\
                                            '<p dir="ltr" style="text-align: left;">' + s_3 + '<br></p>'\
                                                '<br></p>]]></text>\n') 
                                
        f.write('</questiontext>\n')
        f.write('<generalfeedback format="html">\n')
        f.write('<text></text>\n')
        f.write('</generalfeedback>\n')
        f.write('<defaultgrade>' +str(float(points_avail)) +'</defaultgrade>\n')
        f.write('<penalty>0.3333333</penalty>\n')
        f.write('<hidden>0</hidden>\n')
        f.write('<idnumber>' + ID +'</idnumber>\n')
        f.write('<single>false</single>\n')
        f.write('<shuffleanswers>true</shuffleanswers>\n')
        f.write('<answernumbering>abc</answernumbering>\n')
        f.write('<showstandardinstruction>0</showstandardinstruction>\n')
        f.write('<correctfeedback format="html">\n')
        f.write('<text>Die Frage wurde richtig beantwortet.</text>\n')
        f.write('</correctfeedback>\n')
        f.write('<partiallycorrectfeedback format="html">\n')
        f.write('<text>Die Frage wurde teilweise richtig beantwortet.</text>\n')
        f.write('</partiallycorrectfeedback>\n')
        f.write('<incorrectfeedback format="html">\n')
        f.write('<text>Die Frage wurde falsch beantwortet.</text>\n')
        f.write('</incorrectfeedback>\n')
        f.write('<shownumcorrect/>\n')
        
        # Alle richtigen Antworten
        for i in range (0, num_true):
            
            if ans_type=='unit': 
                f.write('<answer fraction="' + perc_true +'" format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;">\\(\\mathrm{' + true_ans[i] + '}\\)<br></p>]]></text>\n')
                f.write('<feedback format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"><span class="" style="color: rgb(152, 202, 62);">richtig</span><br></p>]]></text>\n')
                f.write('</feedback>\n')
                f.write('</answer>\n')
                
            elif ans_type=='math':
                f.write('<answer fraction="' + perc_true +'" format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;">\\(' + true_ans[i] + '\\)<br></p>]]></text>\n')
                f.write('<feedback format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"><span class="" style="color: rgb(152, 202, 62);">richtig</span><br></p>]]></text>\n')
                f.write('</feedback>\n')
                f.write('</answer>\n')
                
                
            elif ans_type=='text':
                f.write('<answer fraction="' + perc_true +'" format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;">' + true_ans[i] + '<br></p>]]></text>\n')
                f.write('<feedback format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"><span class="" style="color: rgb(152, 202, 62);">richtig</span><br></p>]]></text>\n')
                f.write('</feedback>\n')
                f.write('</answer>\n')
        
        # Alle falschen Antworten
        for i in range (0, num_false):
            if ans_type=='unit': 
                f.write('<answer fraction="' + perc_false +'" format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;">\\(\\mathrm{' + false_ans[i] + '}\\)<br></p>]]></text>\n')
                f.write('<feedback format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"><span class="" style="color: rgb(239, 69, 64);">falsch</span><br></p>]]></text>\n')
                f.write('</feedback>\n')
                f.write('</answer>\n')
                
            elif ans_type=='math':
                f.write('<answer fraction="' + perc_false +'" format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;">\\(' + false_ans[i] + '\\)<br></p>]]></text>\n')
                f.write('<feedback format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"><span class="" style="color: rgb(239, 69, 64);">falsch</span><br></p>]]></text>\n')
                f.write('</feedback>\n')
                f.write('</answer>\n')
                
            elif ans_type=='text':
                f.write('<answer fraction="' + perc_false +'" format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;">' + false_ans[i] + '<br></p>]]></text>\n')
                f.write('<feedback format="html">\n')
                f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"><span class="" style="color: rgb(239, 69, 64);">falsch</span><br></p>]]></text>\n')
                f.write('</feedback>\n')
                f.write('</answer>\n')    
        
        f.write('</question>\n')
        f.write('</quiz>\n')
    return None

def write_question_NF(save_dir, ID, name, s_1, s_2, s_3, b_str, points_avail, result, pic, tol_abs, picID = None):
    """Funktion schreibt NF-Frage auf Grundlage der übergebenen strings nach Pfad f_path"""
    if picID == None:
        picID = ID
    q_name = ID + '_' + name
    f_path = (save_dir / q_name).with_suffix('.xml')
   
    with open(f_path,'w', encoding='utf-8') as f:
        # Text schreiben
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<quiz>\n')
        f.write('<question type="numerical">\n')
        f.write('<name>\n')
        f.write('<text>' + q_name + '</text>\n')
        f.write('</name>\n')
        f.write('<questiontext format="html">\n')
        if pic != 0:
            f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"> <b>ID '+ str(ID) +' </b> <br></p>'\
                                    '<p dir="ltr" style="text-align: left;">' + s_1 + '<br></p>'\
                                        '<p dir="ltr" style="text-align: left;">' + s_2 + '<br></p>'\
                                            '<p dir="ltr" style="text-align: left;">' + s_3 + b_str +'<br><br></p>'\
                                                '<br><img src="@@PLUGINFILE@@/'+ str(picID) + '.svg" alt="Bild" width="500"><br>'\
                                                    '<br></p>]]></text>\n')
            f.write(pic)
        else:
            f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"> <b>ID '+ID+' </b> <br></p>'\
                                    '<p dir="ltr" style="text-align: left;">' + s_1 + '<br></p>'\
                                        '<p dir="ltr" style="text-align: left;">' + s_2 + '<br></p>'\
                                            '<p dir="ltr" style="text-align: left;">' + s_3 + b_str+ ']]></text>\n') 
                                
        f.write('</questiontext>\n')
        f.write('<generalfeedback format="html">\n')
        f.write('<text></text>\n')
        f.write('</generalfeedback>\n')
        f.write('<defaultgrade>' +str(float(points_avail)) +'</defaultgrade>\n')
        f.write('<penalty>0.3333333</penalty>\n')
        f.write('<hidden>0</hidden>\n')
        f.write('<idnumber>' + ID +'</idnumber>\n')
        f.write('<answer fraction="100" format="moodle_auto_format">\n')
        f.write('<text>'+ str(result) +'</text>\n')
        f.write('<feedback format="html">\n')
        f.write('<text><![CDATA[<p dir="ltr" style="text-align: left;"><span class="" style="color: rgb(152, 202, 62);">Das Ergebnis ist im Rahmen der 1%-Toleranz korrekt.</span><br></p>]]></text>\n')
        f.write('</feedback>\n')
        f.write('<tolerance>'+ str(tol_abs)+'</tolerance>\n')
        f.write('</answer>\n')
        f.write('<unitgradingtype>0</unitgradingtype>\n')
        f.write('<unitpenalty>0.1000000</unitpenalty>\n')
        f.write('<showunits>3</showunits>\n')
        f.write('<unitsleft>0</unitsleft>\n')
        f.write('</question>\n')
        f.write('</quiz>\n')
    return None
