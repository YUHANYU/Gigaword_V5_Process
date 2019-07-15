# -*- coding: UTF-8 -*-

# @ Time         :  2019/7/2
# @ Author       :  Dong Hao, XiaoWei Du, Hanyu Yu
# @ Environment  :  Python 3.7.0 + spaCy 2.1.0 + BeautifulSoup 4.6.3


"""
Program Description
This is the processing code for the English Gigaword 5-th News text data. https://catalog.ldc.upenn.edu/LDC2011T07
The goal of this program is to convert the text into a specific format,
    with one sentence per line, and one blank line between documents.
The news text is divided into story, multi, advis and other types according to the new description.
The processed file is named as original name and the type, such as afp_eng_199405_advis.txt
You only need to give the target file sub-folder in the main function.
The processed files are put in the four type of folder under this project.
Please attention, the project has not finish and may be has some mistake.
Note that this project is still a work in progress.
If you have any idea, please contact with me. yuhanyu@cloudwalk.cn/yuhanyu@m.scnu.edu.cn

代码描述
这是针对English Gigaword 5-th 新闻文本数据的处理代码。 https://catalog.ldc.upenn.edu/LDC2011T07
代码的处理目标是将文本转化为特定的预训练格式，每个文档的每一句为一行，文档和文档之间使用空行分开。
新闻文本按照说明，按照其类型被分为story，multi，advis，other类型，并且被写在指定的文件夹下
处理后的写入文件以：原始文件名+类型.txt命名，如“afp_eng_199405_advis.txt”
只需要在main主函数中给出目标文件子文件夹，如apw_eng，就能被处理。
处理后的文件存放路径为项目路径下的四个类型的子文件。
请注意，当前项目尚未完成，可能存在一些错误。
如果你感到有任何想法，请和我联系。yuhanyu@cloudwalk.cn/yuhanyu@m.scnu.edu.cn
"""

import os

from bs4 import BeautifulSoup

import re

from spacy.lang.en import English


class Process_Docs():

    def __init__(self):
        self.nlp = English(disable=["parser"])
        sentencizer = self.nlp.create_pipe("sentencizer")
        self.nlp.add_pipe(sentencizer)

    def process_story(self, doc):
        paragraphs = doc.find_all('p')  # find all paragraphs
        temp = []
        for index, p in enumerate(paragraphs):
            # limit the length of a paragraph
            if index != len(paragraphs) - 1 or index != len(paragraphs) - 2 and len(p.text) >= 10 and p:
                # replace multiple spaces and remove the front and back spaces
                new_p = re.sub(' +', ' ', p.string.replace('\n', ' ').replace('- ', '-')).lstrip().rstrip()
                if self.has_indexes(new_p):  # judge the original numerals
                    temp.append(new_p)
                    continue
                new_p_s = self.nlp(new_p)  # use spaCy to punctuate sentences
                new_p_s = self.process_marks(new_p_s)  # process the quotation
                for s in new_p_s:
                    temp.append(s)

        temp.append('\n')
        return temp

    def process_multi(self, doc, keyword):
        texts = doc.find_all('text')  # find all texts
        temp = []
        for text in texts:
            if text:
                # use (keyword) to split paragraphs
                news = str(text.string).split('(' + keyword.upper() + ')')
                for index, new in enumerate(news):
                    # if has data
                    if index == 0 and self.has_date(new) and new:
                        new = new.split('\n', 2)[2]  # split text and remove data
                    # replace the return with blank, remove the front and back spaces, and a special case
                    new = re.sub(' +', ' ', new.replace('\n', ' ').replace('- ', '-')).lstrip().rstrip()
                    nlp_news = self.nlp(new)  # use spaCy to punctuate sentences
                    for s in nlp_news.sents:
                        if s and len(s.text) >= 15:  # limit the length of sentence
                            temp.append(s.text)

        temp.append('\n')
        return temp

    def process_other(self, doc):
        texts = doc.find_all('text')
        temp = []
        for text in texts:
            if text is not None:
                new_text = re.sub(' +', ' ', str(text.string).replace('\n', '').replace('- ', '-')).lstrip().rstrip()
                temp.append(new_text)

        temp.append('\n')
        return temp

    # TODO This format is confusing and needs to be dealt with.
    def process_advis(self, doc):
        texts = doc.find_all('text')
        temp = []
        for text in texts:
            if text is not None:
                new_text = re.sub(' +', ' ', str(text.string).replace('\n', '').replace('- ', '-')).lstrip().rstrip()
                temp.append(new_text)

        temp.append('\n')
        return temp

    def has_date(self, str):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            if day in str and 'since' in str:
                return True

        return False

    def has_indexes(self, p):
        indexes = [str(i) for i in range(100)]
        index_num = 0
        for i in indexes:
            if i in p:
                index_num += 1
                if index_num >= 3:
                    return True
        return False

    def has_index_alphabet(self, target_str):
        index = [i for i in range(1, 15, 1)]
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']

        for i in index:
            for j in alphabet:
                if (str(i) + '. ' + j.upper()) in target_str:
                    return True

        return False

    def process_marks(self, target_strings):
        ss = [i.text for i in target_strings.sents]

        for i in range(len(ss) - 1):
            if ss[i][-1] == '\"' and ss[i][-2] == ' ' and ss[i][-3] == '.':
                ss[i] = ss[i][:-2]
                ss[i + 1] = '\"' + ss[i + 1]

        return ss


class Process_Text():

    def __init__(self, write_path):
        self.doc_obj = Process_Docs()
        self.write_path = write_path

    def get_files_list(self, dir, Filelist):
        if os.path.isfile(dir):
            Filelist.append(dir)
        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                newDir = os.path.join(dir, s)
                self.get_files_list(newDir, Filelist)

        return Filelist

    def process_doc(self, file):
        file_contend = open(file, 'r', encoding='utf-8')
        name = str(file).split('\\')[-1]

        bs4_obj = BeautifulSoup(file_contend, 'lxml')
        docs = bs4_obj.find_all('doc')

        texts_story = []
        texts_other = []
        texts_multi = []
        texts_advis = []

        for index, doc in enumerate(docs):
            doc_type = doc.attrs['type']  # get the type of doc

            # judge types and process
            if doc_type == 'story':
                pass
                # texts_story.append(self.doc_obj.process_story(doc))
            elif doc_type == 'other':
                pass
                # texts_other.append(self.doc_obj.process_other(doc))
            elif doc_type == 'multi':
                pass
                # texts_multi.append(self.doc_obj.process_multi(doc, name.split('_')[0]))
            else:
                texts_advis.append(self.doc_obj.process_advis(doc))

        # self.write_file(texts_story, name, type='story')
        # self.write_file(texts_multi, name, type='multi')
        self.write_file(texts_advis, name, type='advis')
        # self.write_file(texts_other, name, type='other')

    def write_file(self, texts, file_name, type):
        if not os.path.exists(self.write_path + type):
            os.makedirs(self.write_path + type)

        file_write_path = self.write_path + type + '\\'
        with open((file_write_path + str(file_name) + '_' + type + '.txt'), 'w', encoding='utf-8') as file_write:
            for index_1, ss in enumerate(texts):
                for index_2, s in enumerate(ss):
                    file_write.write(s)
                    if index_1 != len(texts) - 1 and index_2 != len(ss) - 1:
                        file_write.write('\n')


def main(data_path, write_path):
    process_obj = Process_Text(write_path)

    files = process_obj.get_files_list(data_path, [])

    for index, e in enumerate(files):
        process_obj.process_doc(e)
        print('The % 3.0f-th file has been read, processed and written correctly ！' % index)


if __name__ == '__main__':
    data_path = os.getcwd() + '\\Data\\data\\xin_eng\\'
    write_path = os.getcwd() + '\\Data\\processed_text\\'
    print('Document Type:', data_path.split('\\')[-2].split('_')[0].upper())
    main(data_path, write_path)
