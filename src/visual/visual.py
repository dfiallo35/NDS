import pandas as pd
import contextlib, io
from compiler.execution import *
import time

from copy import deepcopy


import streamlit as st




class CodeBlock:
    def __init__(self, key: str, code: Code):
        self.code= code
        self.intern_code= deepcopy(self.code)
        self.key= str(key)
        

    def run(self):
        
        self.col1, self.col2, self.col3= st.columns([12, 1, 1])
        
        with self.col1:
            self.script= st.text_area(f'code', key=self.key + '1',
                                    placeholder='code here',
                                    height=200,
                                    label_visibility='hidden',
                                )
            #print all the args of st.text_area
            print(st.text_area.__code__)

        
        with self.col2:
            st.markdown('##')
            st.button('Run', key=self.key + '2', on_click=self.execute)
            st.button('Run All', key=self.key + '3', on_click=self.run_all)
        
        with self.col3:
            st.markdown('##')
            st.button('Add', key=self.key + '5', on_click=self.add_code_block)
            st.button('Delete', key=self.key + '4', on_click=self.delete_code_block)
        
        # with self.col2 and self.col3:
        
        #     st.file_uploader('Upload file', key=self.key + '6', )

        st.markdown('##')
    
    def execute(self):
        self.intern_code= deepcopy(self.code)

        try:
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                self.intern_code.compile(self.script)
            output = f.getvalue()
            self.update()

            with self.col1:
                st.markdown(f'output')
                st.text(output)
        
        except Exception as e:
            with self.col1:
                st.markdown(f'output')
                st.text(e)
    
    def update(self):
        for n, code_block in enumerate(st.session_state.code_blocks):
            if code_block == self:
                for rest in st.session_state.code_blocks[n+1:]:
                    rest.code= deepcopy(self.intern_code)
                break
                    
                
    def run_all(self):
        for n, code_block in enumerate(st.session_state.code_blocks):
            if code_block == self:
                for rest in st.session_state.code_blocks[n:]:
                    rest.execute()
                break

    def add_code_block(self):
        cb= []
        for code_block in st.session_state.code_blocks:
            if code_block == self:
                cb.append(code_block)
                cb.append(CodeBlock(key=time.time(), code=deepcopy(self.intern_code)))
            else:
                cb.append(code_block)

        st.session_state.code_blocks= cb
    
    # def open_file(self):


    def delete_code_block(self):
        if len(st.session_state.code_blocks) == 1:
            return
        
        cb= []
        for code_block in st.session_state.code_blocks:
            if code_block == self:
                continue
            else:
                cb.append(code_block)
        st.session_state.code_blocks= cb


class Visualizer:
    def visualize(self):

        st.set_page_config(
            page_title="NDS",
            layout="wide",
            initial_sidebar_state="collapsed",
        )

        with open('visual\\style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
        if 'code_blocks' not in st.session_state:
            st.session_state.code_blocks= [CodeBlock(key=time.time(), code=Code())]
        st.title('Nations Development Simulator')

        st.sidebar.title('NDS')
        st.sidebar.markdown('Nations Development Simulator')

        for code_block in st.session_state.code_blocks:
            code_block.run()


# import pandas as pd
# import numpy as np

# df = pd.DataFrame(
#    np.random.randn(50, 20),
#    columns=('col %d' % i for i in range(20)))

# st.dataframe(df)


