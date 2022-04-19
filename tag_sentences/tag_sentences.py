from os import listdir
from os.path import isfile, join

class file_operations:
    def read_txt(self, input_file, skip_title):
        output = ""
        with open(input_file, "r", encoding="utf-8") as f:
            if skip_title == 1:
                next(f)
            for line in f:
                output += line
        return output
    def read_entities_to_one_list(self, input_dir):
        output = []
        entity_filenames = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
        skip_title = 1
        for entity_file in entity_filenames:
            output += self.read_txt(input_dir + "\\" + entity_file, skip_title).split("\n")
        output = [i for i in output if i]
        return output

    def write_file(markus_xml, output_file):
        with open(output_file, "w+", encoding="utf-8") as f:
            f.write(markus_xml)


class text_operations:
    def create_list_from_text(data):
        output_list = []
        sentence = ""
        for char in data:
            sentence += char
            if char in ["。", "！","？", "，", "；"]:
                if char in ["。", "！","？"]: sentence += "breaker"
                output_list.append(sentence)
                sentence = ""
        return output_list

    def tag_sentences_by_entity_lists(sentence_list, entity_list):
        output_tag_status_list = []
        for sentence in sentence_list:
            find_entity = 0
            for entity in entity_list:
                if entity in sentence:
                    # print("___")
                    # print(entity)
                    # print(sentence)
                    # print("====")
                    output_tag_status_list.append(1)
                    find_entity = 1
                    break
            if find_entity == 1: continue
            output_tag_status_list.append(0)
        return output_tag_status_list
    
    def create_markus_xml(input_list,tag_status,filename):
        output = ""
        header = r'''<div class="doc" markupfullname="false" markuppartialname="false" markupnianhao="false" markupofficaltitle="false" markupplacename="false" filename="%s" tag="{&quot;info&quot;:{&quot;color&quot;:&quot;#333399&quot;,&quot;buttonName&quot;:&quot;&amp;#(26377);&amp;#(20449);&amp;#(24687);&quot;,&quot;visible&quot;:true,&quot;status&quot;:&quot;bordered&quot;}}"><pre contenteditable="false" dir="ltr">'''
        end = "</span></pre></div>"
        header = header%filename
        tag_begin = '<span class="markup manual unsolved info" type="info" info_id="">'
        tag_end = '</span>'
        line_begin = '</span><span class="passage" type="passage" id="passage%d"><span class="commentContainer" value="[]"><span class="glyphicon glyphicon-comment" type="commentIcon" style="display:none" aria-hidden="true" data-markus-passageid="passage%d"></span></span>'
        # line_end = "</span>"
        line_end = ""
        passage_count = 0
        output += header + line_begin[7:]%(passage_count, passage_count)
        passage_count += 0
        for i in range(len(input_list)):
            if tag_status[i] == 1:
                output += f"{tag_begin}{input_list[i]}{tag_end}"
            else:
                output += input_list[i]
            if "breaker" in input_list[i]:
                #output += line_begin
                output = line_end + output + line_begin%(passage_count, passage_count)
                passage_count += 1
        output = output.replace("breaker", "\n\n") + end
        return output

from os import listdir
from os.path import isfile, join

input_dir = "input"
output_dir = "output"
f_io = file_operations()
text_tools = text_operations
input_file_list = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
for input_file in input_file_list:
    
    input_file_with_path = f'{input_dir}\{input_file}'
    # for single_file
    # read the input data and remove the line breaks
    input_txt = f_io.read_txt(input_file_with_path, 0).replace("\n", "breaker")
    input_txt = input_txt.replace(",", "，")
    input_txt = input_txt.replace("'", "‘")
    input_txt = input_txt.replace("\"", "“")
    while "breakerbreaker" in input_txt:
        input_txt = input_txt.replace("breakerbreaker", "breaker")
    # break sentences to create a list
    input_list = text_operations.create_list_from_text(input_txt)
    # load all the entitie lists
    entity_list = f_io.read_entities_to_one_list("..\cbdb_entities_list")
    # assign tags for the sentences which includes any entities
    tag_status = text_tools.tag_sentences_by_entity_lists(input_list, entity_list)
    filename = input_file.split(".")[0]
    markus_xml = text_tools.create_markus_xml(input_list,tag_status,filename)
    output_filename = f'{output_dir}\{filename}.html'
    file_operations.write_file(markus_xml, output_filename)

