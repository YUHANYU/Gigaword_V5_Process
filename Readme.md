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