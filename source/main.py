# -*- coding: utf-8 -*-
import os
import gradio as gr
from llm_api import get_ans,get_respone

from project_database import *
from ui_backend import *
from config import *

if __name__=="__main__":
    database_list, database_namelist = load_database()
    # ----------------------------------- UI controls define ------------------------------
    input_database_select_report = gr.Dropdown(choices=database_namelist, label="知识库选择", value=database_namelist[0])
    input_prompt = gr.DataFrame(database_list[0].prompt_data, height=400)
    input_uploadbtn = gr.UploadButton(label="上传知识库", file_count="directory")  # 上传文件夹的功能按钮

    input_database_select_QA = gr.Dropdown(choices=database_namelist, label="知识库选择", value=database_namelist[0])

    output_gen_proc = gr.Textbox(label="报告生成过程", lines=11, max_lines=14)
    output_report = gr.Textbox(label="报告生成内容", lines=11, max_lines=14)

    # ------------------------------------ UI Start ---------------------------------
    # Set ui and make the clear Button invisible: clear_btn=gr.Button("clear",visible=False),allow_flagging="never" make clear and flag invisible
    interface_report = gr.Interface(fn=function_report_generation, inputs=[input_database_select_report, input_uploadbtn, input_prompt], outputs=[output_gen_proc, output_report],
                              submit_btn="点击生成报告", clear_btn=gr.Button("clear", visible=False),
                              allow_flagging="never")  #


    interface_QA = gr.Interface(fn=function_QA, inputs=[input_database_select_QA, 'text'], outputs="text", allow_flagging='never')

    # pack interface
    tab_interface = gr.TabbedInterface([interface_report, interface_QA], ["报告生成", "知识库问答"], title="RAG报告生成问答")

    with tab_interface as tab_interface:
        input_database_select_report.change(database_change,input_database_select_report,input_prompt)
        input_uploadbtn.upload(upload,input_uploadbtn,[input_database_select_report,input_prompt])
        tab_interface.launch(server_name="127.0.0.1",server_port=9909,show_api=False)



