# import pandas as pd
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
        self.output= None

    def run(self):
        
        self.col1, self.col2, self.col3= st.columns([12, 1, 1])
        
        with self.col1:
            self.script= st.text_area(f'code', key=self.key + '1',
                                    placeholder='code here',
                                    height=200,
                                    label_visibility='hidden',
                                )

        
        with self.col2:
            st.markdown('##')
            st.button('Run', key=self.key + '2', on_click=self.execute)
            st.button('Run All', key=self.key + '3', on_click=self.run_all)
        
        with self.col3:
            st.markdown('##')
            st.button('Add', key=self.key + '5', on_click=self.add_code_block)
            st.button('Delete', key=self.key + '4', on_click=self.delete_code_block)

        st.markdown('##')
        self.visualize()
    
    def execute(self):
        self.intern_code= deepcopy(self.code)

        try:
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                self.intern_code.compile(self.script)
            self.output = f.getvalue()
            self.update()
        
        except Exception as e:
            with self.col1:
                st.markdown(f'output')
                st.text(e)
    
    def visualize(self):
        with self.col1:
            if self.output:
                if len(self.output.split('\n')) > 40:
                    with st.expander('output', expanded=False):
                        st.text(self.output)
                else:
                    with st.expander('output', expanded=True):
                        st.text(self.output)
            
            for t, g in self.intern_code.plots:
                if t == 'line':
                    st.line_chart(g)
                elif t == 'bar':
                    st.bar_chart(g)
                elif t == 'area':
                    st.area_chart(g)
            for _, d in self.intern_code.dataframes:
                st.dataframe(d.T)
                        
            self.intern_code.plots= []
            self.intern_code.dataframes= []
    
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
        
        st.title('Nations Development Simulator')
        st.sidebar.title('NDS')
        st.sidebar.markdown('Nations Development Simulator')

        if 'code_blocks' not in st.session_state:
            st.session_state.code_blocks= [CodeBlock(key=time.time(), code=Code())]

        for code_block in st.session_state.code_blocks:
            code_block.run()
    
