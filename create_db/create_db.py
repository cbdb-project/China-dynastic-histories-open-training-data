'''
SELECT max(id)+1 AS id FROM `chapters`
UNION
SELECT max(id)+1 AS id FROM `sections`
UNION
SELECT max(id)+1 AS id FROM `main`
'''
config_chapterid_start = 1
config_sectionid_start = 1
config_tagid_start = 1

from os import listdir
from os.path import isfile, join
import csv
import re
from datetime import datetime

class file_operations:
    def read_txt_to_list(self, input_file, breaker):
        def read_txt_to_list_by_lineid(lineid):
            nonlocal input_file
            nonlocal breaker
            output = []
            with open(input_file, "r", encoding="utf-8") as f:
                csv_reader = csv.reader(f, delimiter=breaker)
                for line in csv_reader:
                    if line[lineid] == "": continue
                    output.append(line[lineid])
            return output
        return read_txt_to_list_by_lineid

    def write_txt_file(data, output_file):
        with open(output_file, "w+", encoding="utf-8") as f:
            f.write(data)

    def write_csv_file(data_list, output_file):
        with open(output_file, "w+", encoding="utf-8", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(data_list)

class tag_entities:
    def tag_altnames(sectionid, personid, name, section_content, current_date):
        global config_tagid_start
        output = []
        type = 2
        type_chn = "別名"
        zi = 11
        zi_chn = "字"
        hao = 26
        hao_chn = "室名、別號"
        biehao_chn = "別號"
        xiaozi = 27
        xiaozi_chn = "小字"
        subtype = ""
        matches = re.findall(r'^((字)|(號)|(小字)|(別號))([^,.，。；;\?？!！]{1,10})', section_content)
        if matches!=[]:
            for single_match in matches:
                anchor_word = single_match[0]
                content_word = single_match[5]
                if anchor_word == zi_chn: 
                    subtype = zi
                if anchor_word == hao_chn or anchor_word == biehao_chn:
                    subtype = hao              
                if anchor_word == xiaozi_chn:
                    subtype = xiaozi
                output.append([config_tagid_start, sectionid, personid, name, type, subtype, content_word, content_word, current_date])
                config_tagid_start+=1
        return output

    def tag_biographical_addresses(sectionid, personid, name, section_content, current_date):
        global config_tagid_start
        output = []
        type = 5
        subtype = 13
        exception_list = ["舍", "夫", "舉"]
        matches = re.findall(r'^([^,.，。；;\?？!！]{2,10})(人)[，。]', section_content)
        if matches!=[]:
            for single_match in matches:
                content_word = single_match[0]
                if content_word[-1] in exception_list: continue
                output.append([config_tagid_start, sectionid, personid, name, type, subtype, content_word, content_word, current_date])
                config_tagid_start+=1
        return output
    def tag_entries(sectionid, personid, name, section_content, current_date):
        global input_entry_list
        global config_tagid_start
        type = 4
        subtype = 12
        output =[]
        f_io = file_operations()
        file_reader = f_io.read_txt_to_list(input_entry_list, "\t")
        entry_list = file_reader(0)[1:]
        for entry_name in entry_list:
            if entry_name in section_content:
                output.append([config_tagid_start, sectionid, personid, name, type, subtype, entry_name, entry_name, current_date])
                config_tagid_start+=1
        return output
    def tag_offices(sectionid, personid, name, section_content, current_date):
        global input_office_list
        global config_tagid_start
        type = 3
        subtype = 20
        output =[]
        f_io = file_operations()
        file_reader = f_io.read_txt_to_list(input_office_list, "\t")
        office_list = file_reader(0)[1:]
        # office_list_for_re = ")|(".join(office_list)
        # office_list_for_re = f'(({office_list_for_re}))'
        # matches = re.findall(office_list_for_re, section_content)
        # if matches!=[]:
            # for single_match in matches:
            #     content_word = single_match[0]
            #     output.append([config_tagid_start, sectionid, personid, name, type, subtype, content_word, content_word, current_date])
            #     config_tagid_start+=1
        for office_title in office_list:
            if office_title in section_content:
                output.append([config_tagid_start, sectionid, personid, name, type, subtype, office_title, office_title, current_date])
                config_tagid_start+=1
        return output

class create_data(file_operations, tag_entities):
    def create_chapters(self, chapterid_start, chapter_name_list, book_list, output_chapter_list_file):
        output_list = []
        chapter_id = chapterid_start
        for i in range(len(chapter_name_list)):
            output_list.append([chapter_id, chapter_name_list[i], "", book_list[i]])
            chapter_dictionary[f'{book_list[i]}-{chapter_name_list[i]}'] = chapter_id
            chapter_id+=1
        file_operations.write_csv_file(output_list, output_chapter_list_file)

    def create_tag_columns(self, sectionid, personid, name, section_content):
        global config_tagid_start
        tagged_output = []
        now = datetime.now()
        current_date = now.strftime("%Y%m%d")
        tagged_data = tag_entities.tag_altnames(sectionid, personid, name, section_content, current_date)
        if tagged_data != []: tagged_output+=tagged_data
        tagged_data = tag_entities.tag_biographical_addresses(sectionid, personid, name, section_content, current_date)
        if tagged_data != []: tagged_output+=tagged_data
        tagged_data = tag_entities.tag_entries(sectionid, personid, name, section_content, current_date)
        if tagged_data != []: tagged_output+=tagged_data
        tagged_data = tag_entities.tag_offices(sectionid, personid, name, section_content, current_date)
        if tagged_data != []: tagged_output+=tagged_data
        return tagged_output


    def create_sections_tags(self, sectionid, sections_list, chapter_name, personid, name, book_name, output_sections_list_file, output_tags_list_file):
        global chapter_dictionary
        output_sections_list = []
        output_tags_list = []
        current_counter = 1
        chapter_id = chapter_dictionary[f'{book_name}-{chapter_name}']
        for i in sections_list:
            output_sections_list.append([sectionid, i, chapter_id, personid, name, current_counter])
            tagged_list = self.create_tag_columns(sectionid, personid, name, i)
            if tagged_list!=[]:
                output_tags_list+=tagged_list
            current_counter+=1
            sectionid+=1
        file_operations.write_csv_file(output_sections_list, output_sections_list_file)
        file_operations.write_csv_file(output_tags_list, output_tags_list_file)

input_dir = "input"
name_list_file = f'{input_dir}\\name_list.txt'
input_data_dir = f'{input_dir}\\data'
input_entry_list = '..\cbdb_entities_list\cbdb_entity_entries.csv'
input_office_list = '..\cbdb_entities_list\cbdb_entity_offices.csv'

output_dir = "output"
output_chapter_list_file = f'{output_dir}\\chapters.csv'
output_sections_list_file = f'{output_dir}\\sections.csv'
output_tags_list_file = f'{output_dir}\\main.csv'

chapter_dictionary = {}
f_io = file_operations()
create_data_class = create_data()
file_reader = f_io.read_txt_to_list(name_list_file, "\t")

# Get person name list from name_list
name_list = file_reader(1)
# Get personid name list from name_list
personid_list = file_reader(2)
# Get book name list from name_list
book_list = file_reader(7)
# Get chapter name list from name_list
chapter_name_list = file_reader(8)
# Create chapters table
create_data_class.create_chapters(config_chapterid_start, chapter_name_list, book_list, output_chapter_list_file)

for i in range(len(name_list)):
    file_reader = f_io.read_txt_to_list(f"{input_data_dir}\{personid_list[i]}.data.txt", ",")
    # Get section list from input/data and also remove the table heads
    sections_list = file_reader(3)[1:]
    # Create sections table
    create_data_class.create_sections_tags(config_sectionid_start, sections_list, chapter_name_list[i], personid_list[i], name_list[i], book_list[i], output_sections_list_file, output_tags_list_file)


