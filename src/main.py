#todo: generar ejemplo de simulacion
import pandas as pd
import contextlib, io
from execution import *
import time


import streamlit as st
st.set_page_config(
        page_title="NDS",
        layout="wide",
        initial_sidebar_state="expanded",
    )



class CodeBlock:
    def __init__(self, key: str, code: Code):
        self.code= code
        self.intern_code= copy(self.code)
        self.key= str(key)
        

    def run(self):
        self.col1, self.col2= st.columns([10,1])
        
        with self.col1:
            em= st.empty()
            self.script= em.text_area(f'code', key=self.key + '1', placeholder='code here', height=200)

        
        with self.col2:
            st.markdown('##')
            st.button('Run', key=self.key + '2', on_click=self.execute)
            st.button('Run All', key=self.key + '3', on_click=self.run_all)
            st.button('Delete', key=self.key + '4', on_click=self.delete_code_block)
            st.button('Add', key=self.key + '5', on_click=self.add_code_block)

        st.markdown('##')
    
    def execute(self):
        self.intern_code= copy(self.code)

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
                for rest in st.session_state.code_blocks[n:]:
                    rest.code= copy(self.intern_code)
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
                cb.append(CodeBlock(key=time.time(), code=copy(self.intern_code)))
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

Visualizer().visualize()
