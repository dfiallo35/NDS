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



@st.cache(allow_output_mutation=True)
def map(map: Map):
    return map


class CodeBlock:
    def __init__(self, code: Code, number: int, script: str= ''):
        self.code= code
        self.number= number
        self.intern_code= copy(self.code)
        self.script= script
        
        

    def run(self):
        self.col1, self.col2= st.columns([10,1])
        
        with self.col1:
            em= st.empty()
            self.script= em.text_area(f'code', key=f'code {self.number}', placeholder='code here', height=200, value=self.script, label_visibility='hidden')

        
        with self.col2:
            st.markdown('##')
            st.button('Run', key=f'Run {self.number}', on_click=self.execute)
            st.button('Delete', key=f'Delete {self.number}', on_click=self.delete_code_block)
            st.button('Add', key=f'Add {self.number +1}', on_click=self.add_code_block)

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
        for code_block in st.session_state.code_blocks:
            if code_block.number > self.number:
                code_block.code= copy(self.intern_code)
                
        

    def add_code_block(self):
        cb= []
        for code_block in st.session_state.code_blocks:
            if code_block.number == self.number:
                cb.append(CodeBlock(copy(code_block.code), code_block.number, code_block.script))

                rest_code_blocks= [(copy(i.code), i.number, i.script)for i in st.session_state.code_blocks[self.number+1:]]
                st.session_state.code_blocks.clear()
                if len(rest_code_blocks) == 0:
                    cb.append(CodeBlock(copy(self.intern_code), self.number +1))
                    break

                for above_code_block in rest_code_blocks:
                    if above_code_block[1] == self.number +1:
                        
                        temp_cb= CodeBlock(copy(self.intern_code), above_code_block[1], '')
                        cb.append(temp_cb)

                        temp_cb= CodeBlock(copy(self.intern_code), above_code_block[1]+1, above_code_block[2])
                        cb.append(temp_cb)

                    else:
                        temp_cb= CodeBlock(copy(self.intern_code), above_code_block[1]+1, above_code_block[2])
                        cb.append(temp_cb)
                
                break
            else:
                cb.append(CodeBlock(copy(code_block.code), code_block.number, code_block.script))

        st.session_state.code_blocks= cb
    
    #todo: if just one code block, dont delete
    def delete_code_block(self):
        cb= []
        if len(st.session_state.code_blocks) == 1:
            return
        for code_block in st.session_state.code_blocks:
            if code_block.number == self.number:
                rest_code_blocks= [(copy(i.code), i.number, i.script)for i in st.session_state.code_blocks[self.number+1:]]
                st.session_state.code_blocks.clear()
                if len(rest_code_blocks) == 0:
                    break

                for above_code_block in rest_code_blocks:
                    temp_cb= CodeBlock(copy(self.intern_code), above_code_block[1]-1, above_code_block[2])
                    cb.append(temp_cb)
                
                break
            else:
                cb.append(CodeBlock(copy(code_block.code), code_block.number, code_block.script))

        st.session_state.code_blocks= cb


class Visualizer:
    def visualize(self):
        if 'code_blocks' not in st.session_state:
            st.session_state.code_blocks= [CodeBlock(Code(), 0)]
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
