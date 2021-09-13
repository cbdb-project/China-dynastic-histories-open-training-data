from os import listdir
from os.path import isfile, join
import uuid

filename = str(uuid.uuid4())
class file_operations:
    def read_txt(self, input_file):
        output = ""
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                output += line
        return output
    def read_entities_to_one_list(self, input_dir):
        output = []
        entity_filenames = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
        for entity_file in entity_filenames:
            output += self.read_txt(input_dir + "\\" + entity_file).split("\n")
        output = [i for i in output if i]
        return output

    def write_file(markus_xml, output_file):
        global filename
        filename += ".html"
        with open(filename, "w+", encoding="utf-8") as f:
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
    
    def create_markus_xml(input_list,tag_status):
        output = ""
        header = r'''<div class="doc" markupfullname="false" markuppartialname="false" markupnianhao="false" markupofficaltitle="false" markupplacename="false" filename="%s" tag="{&quot;info&quot;:{&quot;color&quot;:&quot;#333399&quot;,&quot;buttonName&quot;:&quot;&amp;#(26377);&amp;#(20449);&amp;#(24687);&quot;,&quot;visible&quot;:true,&quot;status&quot;:&quot;bordered&quot;},&quot;fullName&quot;:{&quot;buttonName&quot;:&quot;&amp;#(22995);&amp;#(21517);&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#d9534f&quot;,&quot;status&quot;:&quot;&quot;},&quot;partialName&quot;:{&quot;buttonName&quot;:&quot;&amp;#(21029);&amp;#(21517);&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#f0ad4e&quot;,&quot;status&quot;:&quot;&quot;},&quot;placeName&quot;:{&quot;buttonName&quot;:&quot;&amp;#(22320);&amp;#(21517);&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#428bca&quot;,&quot;status&quot;:&quot;&quot;},&quot;officialTitle&quot;:{&quot;buttonName&quot;:&quot;&amp;#(23448);&amp;#(21517);&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#5bc0de&quot;,&quot;status&quot;:&quot;&quot;},&quot;timePeriod&quot;:{&quot;buttonName&quot;:&quot;&amp;#(26178);&amp;#(38291);&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;green&quot;,&quot;status&quot;:&quot;&quot;},&quot;comparativeus&quot;:{&quot;buttonName&quot;:&quot;comparativus&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;green&quot;,&quot;status&quot;:&quot;&quot;},&quot;dilaPerson&quot;:{&quot;buttonName&quot;:&quot;dilaPerson&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#d6616b&quot;,&quot;status&quot;:&quot;&quot;},&quot;dilaPlace&quot;:{&quot;buttonName&quot;:&quot;dilaPlace&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#6b6ecf&quot;,&quot;status&quot;:&quot;&quot;},&quot;koreanPerson&quot;:{&quot;buttonName&quot;:&quot;KPerson&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#b94a48&quot;,&quot;status&quot;:&quot;&quot;},&quot;koreanBook&quot;:{&quot;buttonName&quot;:&quot;KBook&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#428bca&quot;,&quot;status&quot;:&quot;&quot;},&quot;koreanPlace&quot;:{&quot;buttonName&quot;:&quot;KPlace&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#42ca86&quot;,&quot;status&quot;:&quot;&quot;},&quot;koreanOfficialTitle&quot;:{&quot;buttonName&quot;:&quot;KOfficialTitle&quot;,&quot;visible&quot;:true,&quot;color&quot;:&quot;#17becf&quot;,&quot;status&quot;:&quot;&quot;}}"><pre contenteditable="false" dir="ltr">'''
        end = "</pre></div>"
        header = header%filename
        output += header
        tag_begin = '<span class="markup manual unsolved info" type="info" info_id="">'
        tag_end = '</span>'
        line_begin = '<span class="passage" type="passage" id="passage%s"><span class="commentContainer" value="[]"><span class="glyphicon glyphicon-comment" type="commentIcon" style="display:none" aria-hidden="true" data-markus-passageid="passage%s"></span></span></span>'
        for i in range(len(input_list)):
            if tag_status[i] == 1:
                output += f"{tag_begin}{input_list[i]}{tag_end}"
            else:
                output += input_list[i]
            if "breaker" in input_list[i]:
                output += line_begin
        output = output.replace("breaker", "\n\n") + end
        return output


f_io = file_operations()
text_tools = text_operations

# read the input data and remove the line breaks
input_txt = f_io.read_txt("input.txt").replace("\n", "breaker")
while "breakerbreaker" in input_txt:
    input_txt = input_txt.replace("breakerbreaker", "breaker")
# break sentences to create a list
input_list = text_operations.create_list_from_text(input_txt)
# load all the entitie lists
entity_list = f_io.read_entities_to_one_list("..\cbdb_entities_list")
# assign tags for the sentences which includes any entities
tag_status = text_tools.tag_sentences_by_entity_lists(input_list, entity_list)
markus_xml = text_tools.create_markus_xml(input_list,tag_status)
file_operations.write_file(markus_xml, "output.txt")

