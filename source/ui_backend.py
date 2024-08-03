# -*- coding: utf-8 -*-
from llm_api import get_respone
import jieba.analyse as aly
from collections import Counter
import os
import shutil
from project_database import Porject_DataBase,database_namelist,database_list

def function_report_generation(name,input3,input2):
    global database_list,database_namelist

    database = database_list[database_namelist.index(name)]

    result1 = []
    result2 = []

    result1.append("内容解析中......")

    yield "\n".join(result1), "\n".join(result2)

    all_report = ""
    for p_n, group in database.prompt_data.groupby("段落"):
        result1.append(f"第{p_n}段内容生成中......")
        yield "\n".join(result1), "\n".join(result2)
        p_n_content = []
        for question in group["prompt"]:
            search_result = database.search(question, 1)

            # print("向量库检索内容：", search_result)
            search_result = "\n".join(search_result)

            prompt = f"请根据已知内容简洁明了的回复用户的问题，已知内容如下：```{search_result}```,用户的问题是：{question}，如何已知内容无法回答用户的问题，请直接回复：不知道，无需输出其他内容"

            # generate word one by one
            response = get_respone(prompt)
            result1.append("大模型检索及回答内容:\n")
            for trunk in response:
                result1[-1] += trunk.choices[0].delta.content
                yield "\n".join(result1), "\n".join(result2)

            result1[-1] = result1[-1].replace("\n", "")
            p_n_content.append(result1[-1])

            # result1.append(f"大模型检索及回答内容：{result1[-1] }")
            yield "\n".join(result1), "\n".join(result2)

        prompt_report = f"你是一个大学教授，你需要根据相关内容，来写一段内容，生成的内容必须严格来自相关内容，语言必须严谨、符合事实，并且不能使用第一人称，相关内容如下：\n```{''.join(p_n_content)}"
        result1.append(f"第{p_n}段报告内容：\n")
        result2.append(f"\t\t\t")
        yield "\n".join(result1), "\n".join(result2)

        response = get_respone(prompt_report)

        for trunk in response:
            result1[-1] += trunk.choices[0].delta.content  # 每次添加在末尾
            result2[-1] += trunk.choices[0].delta.content  # 每次添加在末尾

            result1[-1] = result1[-1].replace("\n", "")
            result2[-1] = result2[-1].replace("\n", "")
            yield "\n".join(result1), "\n".join(result2)

        all_report += ("    " + "".join(result2[-1]))
        all_report += "\n"

        result1.append("*" * 30)

        yield "\n".join(result1), "\n".join(result2)


def function_QA(name,text):
    global database_list, database_namelist
    database = database_list[database_namelist.index(name)]

    result = [""]

    search_result = database.search(text,3)
    search_result = "\n".join(search_result)

    prompt = f"请根据已知内容简洁明了的回复用户的问题，已知内容如下：```{search_result}```,用户的问题是：{text}，如何已知内容无法回答用户的问题，请直接回复：不知道，无需输出其他内容"

    response = get_respone(prompt)

    for trunk in response:
        result[-1] += trunk.choices[0].delta.content
        yield "\n".join(result)


def database_change(name):
    global database_list,database_namelist

    return database_list[database_namelist.index(name)].prompt_data

# retrieve high-frequency words
def get_type_name(files):
    content = []
    for file in files:
        try:
            with open(file.name,encoding="utf-8") as f:
                data = f.readlines(1)
                content.extend(aly.tfidf(data[0]))
        except:
            continue
    count = Counter(content)
    kw = count.most_common(2)

    return "".join([i[0] for i in kw])  # return the top2 frequency words


def upload(files):  # files will be stored in a temporary space on the computer
    global database_list,database_namelist,input1
    # check files
    check_txt = False
    check_prompt_xlsx = False

    for file in files:
        if check_txt and check_prompt_xlsx:
            break
        if file.name.endswith(".txt"):
            check_txt = True
        if file.name.endswith(".xlsx"):
            check_prompt_xlsx = True
    else:
        if check_txt== False:
            raise Exception("请上传包含txt文档的文件夹")
        if check_prompt_xlsx ==  False:
            raise Exception("请上传包含prompt.xlsx文件的文件夹")

    # create dir according to the database uploading
    type_name = get_type_name(files)
    save_path = os.path.join("database_dir",type_name)

    if os.path.exists(save_path) == False:
        os.mkdir(save_path)
        os.mkdir(os.path.join(save_path,"txt"))
    if os.path.exists(os.path.join(save_path,"txt"))==False:
        os.mkdir(os.path.join(save_path,"txt"))

    # Save the file to a specified folder
    for file in files:
        if file.name.endswith(".txt"):
            shutil.copy(file.name,os.path.join(save_path,"txt"))
        elif file.name.endswith("prompt.xlsx"):
            shutil.copy(file.name,save_path)

    # create database
    database = Porject_DataBase(save_path,type_name)
    database_list.append(database)
    database_namelist.append(type_name)
    input1.choices.append((type_name,type_name))    # This is how the dropdown list needs to be passed for it to work properly
    return type_name,database.prompt_data           # show by inputs